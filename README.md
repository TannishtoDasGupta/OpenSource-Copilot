![OpenSource Copilot](docs/assets/opensource-copilot-logo.svg)

# OpenSource Copilot

AI-assisted maintenance workspace for open-source GitHub projects. Triage issues and review pull requests with AI assistance while keeping every repository action under maintainer control.

[![CI](https://github.com/TannishtoDasGupta/OpenSource-Copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/TannishtoDasGupta/OpenSource-Copilot/actions/workflows/ci.yml) [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/)

## MVP features
- Issue triage: summarize, classify, estimate priority, and suggest next steps.
- Pull-request analysis: summarize diffs, identify potential risks, and suggest tests.
- GitHub REST API integration and a responsive browser dashboard.
- Read-only by design: suggestions are never applied automatically.

## Stack
FastAPI, Pydantic, OpenAI Responses API, HTTPX, HTML/CSS/JavaScript, pytest, GitHub Actions.

## Quick start
Requires Python 3.11+.

```bash
git clone https://github.com/TannishtoDasGupta/OpenSource-Copilot.git
cd OpenSource-Copilot
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Set `OPENAI_API_KEY` in `.env`. `GITHUB_TOKEN` is optional and recommended for higher GitHub API limits. `OPENAI_MODEL` defaults to `gpt-5.5`.

Open http://127.0.0.1:8000; API docs: http://127.0.0.1:8000/docs.

## API
- `GET /api/health`
- `POST /api/triage/text` — `{"title":"Bug title","body":"Details"}`
- `POST /api/triage/issue` — `{"owner":"encode","repo":"httpx","issue_number":123}`
- `POST /api/review/pull-request` — `{"owner":"encode","repo":"httpx","pull_number":123}`

Repository content is untrusted input. Diff excerpts are bounded before model submission.

## Deployment
A Render Blueprint is included in [render.yaml](render.yaml). See [deployment instructions](docs/DEPLOYMENT.md) for setup and environment variables.

## Development
```bash
pip install -r requirements-dev.txt
pytest
```

## Limitations and roadmap
This is an early-stage MVP. AI output can be incomplete or incorrect and must be reviewed. It is not a security scanner or a replacement for human code review. Planned: triage history, configurable rules, webhooks, richer test planning, and multi-repository workspaces.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [deployment instructions](docs/DEPLOYMENT.md). No license has been selected yet; normal copyright restrictions apply.
