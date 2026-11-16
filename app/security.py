"""Shared-key protection for the hosted application API."""
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import get_settings

app_key_header = APIKeyHeader(name="X-App-API-Key", auto_error=False)


def require_app_key(api_key: str | None = Security(app_key_header)) -> None:
    """Protect billable AI endpoints; fail closed for missing or weak secrets."""
    configured_key = get_settings().app_api_key
    if len(configured_key) < 32:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Application access is not configured. Set APP_API_KEY to a random value of at least 32 characters.")
    if not api_key or not secrets.compare_digest(api_key, configured_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing application access key.", headers={"WWW-Authenticate": "ApiKey"})
