from pathlib import Path
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import IssueTextRequest, GitHubIssueRequest, PullRequestRequest
from app.services.ai import AIService, ISSUE_INSTRUCTIONS, PR_INSTRUCTIONS
from app.services.github import GitHubService

STATIC_DIR = Path(__file__).parent / "static"
app = FastAPI(title="OpenSource Copilot", description="AI-assisted GitHub issue triage and pull-request analysis.", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "opensource-copilot"}

@app.post("/api/triage/text")
async def triage_text(request: IssueTextRequest):
    try:
        return {"analysis": AIService().analyze(ISSUE_INSTRUCTIONS, f"Issue title:\n{request.title}\n\nIssue body:\n{request.body}")}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {exc}") from exc

@app.post("/api/triage/issue")
async def triage_issue(request: GitHubIssueRequest):
    try:
        issue = await GitHubService().get_issue(request.owner, request.repo, request.issue_number)
        source = (f"Repository: {request.owner}/{request.repo}\nIssue number: {request.issue_number}\nTitle: {issue.get('title', '')}\nAuthor: {issue.get('user', {}).get('login', 'unknown')}\nLabels: {', '.join(x.get('name', '') for x in issue.get('labels', []))}\nBody:\n{(issue.get('body') or '')[:16000]}")
        return {"source": {"title": issue.get("title"), "html_url": issue.get("html_url")}, "analysis": AIService().analyze(ISSUE_INSTRUCTIONS, source)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="GitHub API request failed.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Issue triage failed: {exc}") from exc

@app.post("/api/review/pull-request")
async def review_pull_request(request: PullRequestRequest):
    try:
        data = await GitHubService().get_pull_request(request.owner, request.repo, request.pull_number)
        pr, files = data["pull_request"], data["files"]
        excerpts = []
        for item in files[:20]:
            patch = item.get("patch") or "[Patch unavailable or binary file]"
            excerpts.append(f"File: {item.get('filename')}\nStatus: {item.get('status')}\nChanges: +{item.get('additions', 0)}/-{item.get('deletions', 0)}\nPatch:\n{patch[:3500]}")
        source = f"Repository: {request.owner}/{request.repo}\nPR: #{request.pull_number} {pr.get('title', '')}\nDescription:\n{(pr.get('body') or '')[:5000]}\n\n" + "\n\n".join(excerpts)
        return {"source": {"title": pr.get("title"), "html_url": pr.get("html_url"), "files_considered": len(excerpts)}, "analysis": AIService().analyze(PR_INSTRUCTIONS, source)}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="GitHub API request failed.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"PR analysis failed: {exc}") from exc
