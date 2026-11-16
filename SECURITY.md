# Security Policy

Do not report exploitable vulnerabilities in public issues. Contact the maintainer privately through GitHub's security advisory feature. Include impact, reproduction steps, affected commit/version, and suggested mitigation.

- Store `OPENAI_API_KEY` and `GITHUB_TOKEN` only in environment variables or a secret manager.
- Never commit `.env` files or credentials.
- Treat issue text, PR descriptions, filenames and diffs as untrusted input.
- AI analysis is advisory and must be reviewed by a human.
- The MVP performs read-only GitHub analysis and does not automatically change issues or merge PRs.
