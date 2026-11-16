import httpx
from app.config import get_settings

class GitHubService:
    def __init__(self):
        self.settings = get_settings()

    async def _get(self, path: str):
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.settings.github_token:
            headers["Authorization"] = f"Bearer {self.settings.github_token}"
        url = f"{self.settings.github_api_url.rstrip('/')}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=False) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_issue(self, owner: str, repo: str, number: int):
        data = await self._get(f"repos/{owner}/{repo}/issues/{number}")
        if "pull_request" in data:
            raise ValueError("The selected number is a pull request, not an issue.")
        return data

    async def get_pull_request(self, owner: str, repo: str, number: int):
        pr = await self._get(f"repos/{owner}/{repo}/pulls/{number}")
        files = await self._get(f"repos/{owner}/{repo}/pulls/{number}/files")
        return {"pull_request": pr, "files": files}
