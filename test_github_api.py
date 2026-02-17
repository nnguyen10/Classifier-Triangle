import unittest

from github_api import get_repo_commit_counts


class TestGitHubApiLive(unittest.TestCase):
    """
    LIVE integration-style unit test (hits real GitHub API).

    Warning:
    - Requires internet access.
    - Can fail due to GitHub rate limits, outages, or CI network restrictions.
    """

    def test_live_repo_commit_counts_for_hdnguye_code(self):
        user_id = "nnguyen10"
        results = get_repo_commit_counts(user_id)

        # Basic sanity checks (keep them flexible so the test doesn’t break
        # when you add/delete repos).
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)  # user may have 0 repos; that's still valid

        # If there are repos, validate structure and commit counts
        for item in results:
            # Works whether you returned RepoCommits dataclass or tuples/dicts
            if hasattr(item, "repo") and hasattr(item, "commits"):
                repo_name = item.repo
                commit_count = item.commits
            elif isinstance(item, tuple) and len(item) == 2:
                repo_name, commit_count = item
            elif isinstance(item, dict) and "repo" in item and "commits" in item:
                repo_name = item["repo"]
                commit_count = item["commits"]
            else:
                self.fail(f"Unexpected result item format: {item!r}")

            self.assertIsInstance(repo_name, str)
            self.assertGreater(len(repo_name), 0)
            self.assertIsInstance(commit_count, int)
            self.assertGreaterEqual(commit_count, 0)


if __name__ == "__main__":
    unittest.main()
