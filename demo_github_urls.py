import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER = "nnguyen10"

def get_json(url: str):
    # GitHub wants a User-Agent header; some setups fail without it. Testing Again 
    req = Request(url, headers={"User-Agent": "HW03a-demo"})
    with urlopen(req, timeout=15) as resp:
        data = resp.read().decode("utf-8")
        return json.loads(data)

def main():
    # 1) List repos
    repos_url = f"https://api.github.com/users/{USER}/repos"
    print("REPOS URL:")
    print(repos_url)
    print()

    repos = get_json(repos_url)
    print(f"Repos returned: {len(repos)}")

    if not repos:
        print("No repos found for this user.")
        return

    # Show first few repo names
    repo_names = [r.get("name") for r in repos if isinstance(r, dict)]
    print("First few repo names:")
    for name in repo_names[:5]:
        print(" -", name)
    print()

    # 2) Pick the first repo and show its commits endpoint
    first_repo = repo_names[0]
    commits_url = f"https://api.github.com/repos/{USER}/{first_repo}/commits"
    print("COMMITS URL (for first repo):")
    print(commits_url)
    print()

    commits = get_json(commits_url)
    print(f"Commits returned on this page: {len(commits)}")
    if commits:
        print("Example first commit SHA:", commits[0].get("sha"))

if __name__ == "__main__":
    try:
        main()
    except HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        # GitHub often returns JSON with message—try to show it
        try:
            body = e.read().decode("utf-8")
            print("Body:", body)
        except Exception:
            pass
    except URLError as e:
        print("URLError:", e.reason)
    except Exception as e:
        print("Error:", repr(e))
