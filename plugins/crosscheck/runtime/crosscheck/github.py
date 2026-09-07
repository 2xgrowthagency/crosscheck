"""GitHub result comments through an injected authenticated API, plus worker hooks.

No credential discovery, CLI execution, media uploads, approval reviews or merges.
api(method, route, payload=None) must return parsed JSON and raise on HTTP failure.
"""
import re
from urllib.parse import urlparse


class GitHubTransport:
    def __init__(self, api, read_target, producer_id, worker=None):
        self.api = api
        self.read_target = read_target
        self.producer_id = producer_id
        self.worker = worker
        self.actor_id = api("GET", "user")["id"]

    def current_target(self):
        return self.read_target()

    @staticmethod
    def address(destination):
        match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/(pull|issues)/([1-9][0-9]*)", destination["locator"])
        if not match:
            raise ValueError("an exact GitHub PR/issue URL is required")
        owner, repo, kind, number = match.groups()
        if destination["kind"] != {"pull": "github-pr", "issues": "github-issue"}[kind]:
            raise ValueError("destination kind differs from URL")
        return f"{owner}/{repo}", number

    def verify_destination(self, destination, target):
        if destination["kind"] == "worker-thread":
            return bool(self.worker and destination["locator"] == self.producer_id
                        and self.worker.verify_destination(destination, target))
        repo, number = self.address(destination)
        parsed = urlparse(target["locator"])
        target_repo = "/".join(parsed.path.strip("/").split("/")[:2])
        # Non-GitHub artifact targets require an adapter with its own verified repo binding.
        if parsed.netloc != "github.com" or target_repo.lower() != repo.lower():
            return False
        kind = "pulls" if destination["kind"] == "github-pr" else "issues"
        entity = self.api("GET", f"repos/{repo}/{kind}/{number}")
        if kind == "pulls":
            return entity["head"]["sha"] == target["revision"]
        return "pull_request" not in entity

    def find_owned(self, destination, markers):
        if destination["kind"] == "worker-thread":
            if not self.worker:
                raise ValueError("worker readback adapter unavailable")
            return self.worker.find_owned(destination, markers)
        repo, number = self.address(destination)
        matches = []
        page = 1
        while True:
            comments = self.api("GET", f"repos/{repo}/issues/{number}/comments?per_page=100&page={page}")
            for comment in comments:
                first_line = comment.get("body", "").splitlines()[:1]
                if comment["user"]["id"] == self.actor_id and first_line and first_line[0] in markers:
                    matches.append({"id": comment["id"], "body": comment["body"], "locator": comment["html_url"]})
            if len(comments) < 100:
                break
            page += 1
        if len(matches) > 1:
            raise ValueError("multiple owned result comments require reconciliation")
        return matches[0] if matches else None

    def put(self, destination, existing, body, key):
        if destination["kind"] == "worker-thread":
            if not self.worker:
                raise ValueError("worker write adapter unavailable")
            return self.worker.put(destination, existing, body, key)
        repo, number = self.address(destination)
        if existing:
            response = self.api("PATCH", f"repos/{repo}/issues/comments/{int(existing['id'])}", {"body": body})
        else:
            response = self.api("POST", f"repos/{repo}/issues/{number}/comments", {"body": body})
        # Verify persisted content and immutable author identity before recording success.
        stored = self.api("GET", f"repos/{repo}/issues/comments/{int(response['id'])}")
        if stored["body"] != body or stored["user"]["id"] != self.actor_id:
            raise ValueError("comment readback differs")
        return stored["html_url"]
