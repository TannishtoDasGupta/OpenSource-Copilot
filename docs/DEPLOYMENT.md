# Deployment

## Render (Blueprint)

The repository includes a `render.yaml` Blueprint for a Python web service.

1. Sign in to [Render](https://render.com/).
2. Choose **New → Blueprint** and connect this repository.
3. Review the service named `opensource-copilot` and apply the Blueprint.
4. Add your OpenAI API key when prompted. A GitHub token is optional, but recommended for higher API rate limits.
5. Wait for the first deployment, then open the generated `onrender.com` URL and check `/api/health`.

Keep API keys in Render environment variables. Never commit a real `.env` file or paste secrets into issues or pull requests.

The free instance may spin down when idle, so the first request after inactivity can take longer. The app requires a valid OpenAI API key for AI analysis; the health endpoint only confirms that the service is running.

## Docker

For local container use, copy `.env.example` to `.env`, set `OPENAI_API_KEY`, then run:

```bash
docker compose up --build
```
