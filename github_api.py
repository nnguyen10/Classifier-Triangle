"""
github_api.py

HW03a: Given a GitHub user ID, return a list of repo names and commit counts.

Design-for-test choices:
- Dependency injection: caller can pass in a "get" function (e.g., requests.get),
  which makes unit tests easy (no real network calls).
- Small functions with clear responsibilities:
  - fetch_all_repos(): pagination for repos
  - get_commit_count(): count commits (uses Link header when possible)
  - get_repo_commit_counts(): orchestrates the output structure
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple
import re

import requests


DEFAULT_TIMEOUT_SECONDS = 10


class GitHubApiError(RuntimeError):
    """Raised when GitHub API returns an error or unexpected response."""


@dataclass(frozen=True)
class RepoCommits:
    repo: str
    commits: int


def _raise_for_status(resp: requests.Response, url: str) -> None:
    """Convert HTTP errors into a helpful exception for this assignment."""
    if resp.status_code >= 400:
        # GitHub often returns useful JSON; keep it simple but informative.
        raise GitHubApiError(f"GitHub API error {resp.status_code} for URL: {url}")


def _parse_link_last_page(link_header: str) -> Optional[int]:
    """
    Parse GitHub Link header and return the 'last' page number if present.

    Example Link header (simplified):
      <https://api.github.com/.../commits?per_page=1&page=2>; rel="next",
      <https://api.github.com/.../commits?per_page=1&page=34>; rel="last"

    Returns:
      int page number if rel="last" exists, else None
    """
    # Find the segment that contains rel="last"
    # and extract page=<N> from its URL.
    parts = [p.strip() for p in link_header.split(",")]
    for part in parts:
        if 'rel="last"' in part:
            m = re.search(r"[?&]page=(\d+)", part)
            if m:
                return int(m.group(1))
    return None


def fetch_all_repos(
    user_id: str,
    get: Callable[..., requests.Response] = requests.get,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> List[str]:
    """
    Fetch all repository names for a GitHub user (handles pagination).

    Returns:
      List of repo names (strings).
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id must be a non-empty string")

    repos: List[str] = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/users/{user_id}/repos"
        resp = get(url, params={"per_page": per_page, "page": page}, timeout=timeout)
        _raise_for_status(resp, url)

        data = resp.json()
        if not isinstance(data, list):
            raise GitHubApiError("Unexpected response format for repos (expected a list).")

        if not data:
            break

        for repo_obj in data:
            # GitHub uses "name" (lowercase) in the JSON payload.
            name = repo_obj.get("name")
            if isinstance(name, str):
                repos.append(name)

        # Pagination: if fewer than per_page returned, we’re done.
        if len(data) < per_page:
            break

        page += 1

    return repos


def get_commit_count(
    user_id: str,
    repo: str,
    get: Callable[..., requests.Response] = requests.get,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> int:
    """
    Get number of commits for a repo.

    Efficient approach:
    - Request commits with per_page=1. If Link header has rel="last",
      then last page number == total commits (because 1 commit per page).
    - If no Link header, fall back to len(response_json).

    Note:
    - This counts commits visible via the default branch and GitHub API paging behavior.
    """
    if not repo or not repo.strip():
        raise ValueError("repo must be a non-empty string")

    url = f"https://api.github.com/repos/{user_id}/{repo}/commits"
    resp = get(url, params={"per_page": 1, "page": 1}, timeout=timeout)
    _raise_for_status(resp, url)

    link = resp.headers.get("Link", "")
    if link:
        last_page = _parse_link_last_page(link)
        if last_page is not None:
            return last_page  # per_page=1 => last page number == total commits

    data = resp.json()
    if not isinstance(data, list):
        # Could be an error JSON object even with 200 in rare cases; keep it strict.
        raise GitHubApiError("Unexpected response format for commits (expected a list).")

    return len(data)


def get_repo_commit_counts(
    user_id: str,
    get: Callable[..., requests.Response] = requests.get,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> List[RepoCommits]:
    """
    Main HW function:
      Input: GitHub user ID
      Output: list of (repo name, number of commits)

    Returns:
      List[RepoCommits]
    """
    repo_names = fetch_all_repos(user_id=user_id, get=get, timeout=timeout)

    results: List[RepoCommits] = []
    for repo in repo_names:
        count = get_commit_count(user_id=user_id, repo=repo, get=get, timeout=timeout)
        results.append(RepoCommits(repo=repo, commits=count))

    return results


def format_repo_commit_counts(results: List[RepoCommits]) -> str:
    """
    Convenience formatting to match the assignment output example.
    """
    lines = [f"Repo: {r.repo} Number of commits: {r.commits}" for r in results]
    return "\n".join(lines)


if __name__ == "__main__":
    # Simple manual run (not used by unit tests)
    uid = "nnguyen10"
    out = get_repo_commit_counts(uid)
    print(format_repo_commit_counts(out))
