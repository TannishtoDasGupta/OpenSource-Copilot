# Deployment

## Render Blueprint

1. Sign in to [Render](https://render.com/).
2. Choose **New → Blueprint** and connect this GitHub repository.
3. Review the `opensource-copilot` service and apply the Blueprint.
4. Add these secret environment variables in the Render service settings:
   - `APP_API_KEY`: random secret of at least 32 characters. Generate locally with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
   - `OPENAI_API_KEY`: your OpenAI API key.
   - `GITHUB_TOKEN`: optional fine-grained token with read-only access.
5. Wait for deployment and confirm `/api/health` returns healthy.
6. Open the generated HTTPS URL and enter the same `APP_API_KEY` in the dashboard.

Never put provider secrets in Git, frontend code, issue comments, or pull requests. Configure them only in the hosting provider's secret environment settings. Rotate exposed keys immediately.

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `APP_API_KEY` | Yes | Protects billable analysis endpoints; use at least 32 random characters |
| `OPENAI_API_KEY` | Yes for AI analysis | Server-side OpenAI API access |
| `GITHUB_TOKEN` | Optional | Higher GitHub API limits; use read-only scope |
| `OPENAI_MODEL` | No | Defaults to the model configured in app settings |

The dashboard keeps the app key in the current browser session and sends it in the `X-App-API-Key` header. It never receives the server-side OpenAI or GitHub provider keys.

## Local Docker

```bash
cp .env.example .env
# Set APP_API_KEY and OPENAI_API_KEY in .env
docker compose up --build
```

The Compose port binds to localhost only. This is a local development setup, not an internet-facing deployment.

## Operational notes

- Render's free service may spin down when idle.
- OpenAI usage is billed separately. Set provider-side usage limits and monitor spend.
- The shared app key is not user identity, rate limiting, or per-user quotas.
- The app is read-only with respect to GitHub.
