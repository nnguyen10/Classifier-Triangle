import unittest
from unittest.mock import patch, Mock
from github_api import get_repo_commit_counts

class TestGitHubApiMocking(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_two_repos_commit_counts(self, mock_get):
        # Mock response for /users/<id>/repos
        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.json.return_value = [
            {"name": "Triangle567"},
            {"name": "Square567"},
        ]

        # Mock response for /repos/<id>/<repo>/commits with per_page=1
        # Use Link header so commit count comes from rel="last"
        tri_commits_resp = Mock()
        tri_commits_resp.status_code = 200
        tri_commits_resp.headers = {
            "Link": '<https://api.github.com/repos/testuser/Triangle567/commits?per_page=1&page=10>; rel="last"'
        }
        tri_commits_resp.json.return_value = [{}]

        sq_commits_resp = Mock()
        sq_commits_resp.status_code = 200
        sq_commits_resp.headers = {
            "Link": '<https://api.github.com/repos/testuser/Square567/commits?per_page=1&page=27>; rel="last"'
        }
        sq_commits_resp.json.return_value = [{}]

        # Order your code calls requests.get:
        # 1) repos list
        # 2) commits for Triangle567
        # 3) commits for Square567
        mock_get.side_effect = [repos_resp, tri_commits_resp, sq_commits_resp]

        results = get_repo_commit_counts("testuser")

        results_map = {r.repo: r.commits for r in results}
        self.assertEqual(results_map["Triangle567"], 10)
        self.assertEqual(results_map["Square567"], 27)
        self.assertEqual(mock_get.call_count, 3)

    @patch("github_api.requests.get")
    def test_user_not_found_returns_empty_list(self, mock_get):
        # fetch_all_repos will raise GitHubApiError on 404 in your code,
        # so we expect an exception (not empty list).
        resp = Mock()
        resp.status_code = 404
        resp.json.return_value = {"message": "Not Found"}
        mock_get.return_value = resp

        with self.assertRaises(Exception):
            get_repo_commit_counts("missinguser")

if __name__ == "__main__":
    unittest.main()
