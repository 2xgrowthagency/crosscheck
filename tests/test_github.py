import sys
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/crosscheck/runtime"))
from crosscheck.github import GitHubTransport


class GitHubTests(unittest.TestCase):
    def setUp(self):
        self.dest = dict(id="pr", kind="github-pr", locator="https://github.com/example/demo/pull/1", authorized=True)
        self.target = dict(locator="https://github.com/example/demo", revision="abc")
        self.calls = []
        self.comments = []
        self.transport = GitHubTransport(self.api, lambda: self.target, "producer")

    def api(self, method, route, payload=None):
        self.calls.append((method, route, payload))
        if route == "user": return {"id": 7}
        if route.endswith("pulls/1"): return {"head": {"sha": "abc"}}
        if route.endswith("issues/1"): return {"number": 1}
        if "?per_page" in route:
            page = int(route.split("page=")[-1]); return self.comments[(page-1)*100:page*100]
        if method in ("POST", "PATCH"):
            item = dict(id=123, user={"id":7}, body=payload["body"], html_url="https://github.com/example/demo/pull/1#issuecomment-123")
            self.comments = [item]
            return item
        if route.endswith("issues/comments/123"): return self.comments[0]
        raise AssertionError((method, route))

    def test_binding_rejects_wrong_repository_head_and_kind(self):
        self.assertTrue(self.transport.verify_destination(self.dest, self.target))
        self.assertFalse(self.transport.verify_destination(self.dest, {**self.target, "revision":"new"}))
        self.assertFalse(self.transport.verify_destination(self.dest, {**self.target, "locator":"https://github.com/other/demo"}))
        with self.assertRaises(ValueError): self.transport.verify_destination({**self.dest, "kind":"github-issue"}, self.target)
        self.assertFalse(self.transport.verify_destination(dict(kind="worker-thread",locator="producer"),self.target))

    def test_pagination_actor_and_legacy_marker(self):
        self.comments = [dict(id=i,user={"id":99},body="marker",html_url="https://example.test") for i in range(100)]
        self.comments.append(dict(id=123,user={"id":7},body="legacy-marker\nold result",html_url="https://example.test/123"))
        found = self.transport.find_owned(self.dest, ["marker", "legacy-marker"])
        self.assertEqual(123,found["id"])
        self.assertTrue(any("page=2" in c[1] for c in self.calls))
        self.comments.append(dict(id=124,user={"id":7},body="marker",html_url="https://example.test/124"))
        with self.assertRaises(ValueError): self.transport.find_owned(self.dest,["marker","legacy-marker"])

    def test_create_update_and_persisted_readback_use_only_comment_routes(self):
        location = self.transport.put(self.dest,None,"marker\nPASS","marker")
        self.assertTrue(location.endswith("123"))
        existing = self.transport.find_owned(self.dest,["marker"])
        self.transport.put(self.dest,existing,"marker\nFAIL","marker")
        self.assertEqual("marker\nFAIL",self.comments[0]["body"])
        self.assertEqual(["POST","PATCH"],[c[0] for c in self.calls if c[0] != "GET"])
        self.assertEqual("GET", self.calls[-1][0])


if __name__ == "__main__": unittest.main()
