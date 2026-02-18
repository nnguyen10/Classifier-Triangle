"""
Unit tests for github_api.py using mocking.

These tests avoid real network calls by injecting a mocked "get" function
into get_repo_commit_counts(), which is supported by the code design.
"""

import unittest
<<<<<<< Updated upstream
<<<<<<< Updated upstream

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
=======
from unittest.mock import Mock

from github_api import get_repo_commit_counts, GitHubApiError


class TestGitHubApiMocking(unittest.TestCase):
    """Test cases for GitHub API commit counting using injected mocks."""

=======
from unittest.mock import Mock

from github_api import get_repo_commit_counts, GitHubApiError


class TestGitHubApiMocking(unittest.TestCase):
    """Test cases for GitHub API commit counting using injected mocks."""

>>>>>>> Stashed changes
    def test_two_repos_commit_counts(self):
        """Test commit counts for two repositories using mocked responses."""
        # Mock response for /users/<id>/repos
        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.json.return_value = [
            {"name": "Triangle567"},
            {"name": "Square567"},
        ]

        # Mock responses for /repos/<id>/<repo>/commits?per_page=1&page=1
        # Link header rel="last" determines commit count (page number).
        tri_commits_resp = Mock()
        tri_commits_resp.status_code = 200
        tri_commits_resp.headers = {
            "Link": (
                '<https://api.github.com/repos/testuser/Triangle567/commits?per_page=1&page=10>; rel="last"'
            )
        }
        tri_commits_resp.json.return_value = [{}]

        sq_commits_resp = Mock()
        sq_commits_resp.status_code = 200
        sq_commits_resp.headers = {
            "Link": (
                '<https://api.github.com/repos/testuser/Square567/commits?per_page=1&page=27>; rel="last"'
            )
        }
        sq_commits_resp.json.return_value = [{}]

        # This mock will be called 3 times:
        # 1) repos list
        # 2) commits Triangle567
        # 3) commits Square567
        mock_get = Mock(side_effect=[repos_resp, tri_commits_resp, sq_commits_resp])

        results = get_repo_commit_counts("testuser", get=mock_get)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

            self.assertIsInstance(repo_name, str)
            self.assertGreater(len(repo_name), 0)
            self.assertIsInstance(commit_count, int)
            self.assertGreaterEqual(commit_count, 0)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
    def test_user_not_found_raises(self):
        """Test behavior when GitHub user is not found (404)."""
        resp = Mock()
        resp.status_code = 404
        resp.json.return_value = {"message": "Not Found"}
        resp.headers = {}
<<<<<<< Updated upstream

        mock_get = Mock(return_value=resp)

        with self.assertRaises(GitHubApiError):
            get_repo_commit_counts("missinguser", get=mock_get)

>>>>>>> Stashed changes
=======

        mock_get = Mock(return_value=resp)

        with self.assertRaises(GitHubApiError):
            get_repo_commit_counts("missinguser", get=mock_get)

>>>>>>> Stashed changes

if __name__ == "__main__":
    unittest.main()
