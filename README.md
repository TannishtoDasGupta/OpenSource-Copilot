![OpenSource Copilot](docs/assets/opensource-copilot-logo.svg)

# OpenSource Copilot

AI-assisted maintenance workspace for open-source GitHub projects. Triage issues and review pull requests with AI assistance while keeping every repository action under maintainer control.

[![CI](https://github.com/TannishtoDasGupta/OpenSource-Copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/TannishtoDasGupta/OpenSource-Copilot/actions/workflows/ci.yml) [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/)

## Features

- Issue triage: summarize, classify, estimate priority, and suggest next steps.
- Pull-request analysis: summarize diffs, identify potential risks, and suggest tests.
- GitHub REST API integration and responsive browser dashboard.
- Protected analysis endpoints using a separate application access key.
- Read-only by design: suggestions are never applied automatically.

## Stack

FastAPI, Pydantic Settings, OpenAI Responses API, HTTPX, HTML/CSS/JavaScript, pytest, GitHub Actions.

## Local setup

Requires Python 3.11+.

```bash
git clone https://github.com/TannishtoDasGupta/OpenSource-Copilot.git
cd OpenSource-Copilot
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

Generate a random application access key (at least 32 characters) and set it as `APP_API_KEY`. Set `OPENAI_API_KEY` to enable AI analysis. `GITHUB_TOKEN` is optional and recommended for higher GitHub API limits.

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Start with `uvicorn app.main:app --reload`, open http://127.0.0.1:8000, and enter the `APP_API_KEY` in the dashboard. The key is kept only in the current browser session. API docs: http://127.0.0.1:8000/docs.

## API

- `GET /api/health` — public liveness check.
- `POST /api/triage/text`
- `POST /api/triage/issue`
- `POST /api/review/pull-request`

All analysis endpoints require `X-App-API-Key`. The server-side OpenAI key is never sent to the browser.

## Docker

Copy `.env.example` to `.env`, set `APP_API_KEY` and `OPENAI_API_KEY`, then run `docker compose up --build`. The Compose port binds to localhost for local development.

## Deploy to Render

A Render Blueprint is included in `render.yaml`.

1. Push or merge the repository changes to GitHub.
2. Sign in to Render and choose **New → Blueprint**.
3. Connect this repository and review the `opensource-copilot` service.
4. Add `APP_API_KEY` (random secret), `OPENAI_API_KEY`, and optionally `GITHUB_TOKEN` in the service environment settings.
5. Deploy and wait for the `/api/health` check to pass.
6. Open the generated HTTPS URL and enter the same `APP_API_KEY` in the dashboard.

Use a fine-grained GitHub token with read-only access only. Never put real keys in Git. OpenAI API usage is billed separately; set provider-side usage limits. The shared app key is not user accounts, rate limiting, or per-user quotas. Render's free instance may spin down when idle.

See [deployment instructions](docs/DEPLOYMENT.md).

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Security and limitations

- `APP_API_KEY` protects billable analysis endpoints; rotate it if exposed.
- `OPENAI_API_KEY` stays server-side. A GitHub token should be fine-grained and read-only.
- Use HTTPS for hosted deployments. Do not expose the development server directly to the internet.
- AI output can be incomplete or incorrect and must be reviewed. This is not a security scanner or replacement for human review.
- The app fetches GitHub issues and pull-request diffs but never creates comments, labels, commits, branches, or pull requests.
- Rate limiting, per-user quotas, monitoring, persistent history, webhooks, and multi-repository workspaces remain future enhancements.

See [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), and [SECURITY.md](SECURITY.md). MIT licensed.
