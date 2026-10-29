# ==============================================================================
# File: .//Description-of-file/auth_service.md
# Overview: Provides admin authentication verification via constant-time comparison.
# ==============================================================================

import secrets
from typing import Optional
from fastapi import Header, HTTPException, status
from config import settings


def verify_admin_key(
    x_admin_key: Optional[str] = Header(
        default=None,
        alias="X-Admin-Key",
        description="Admin passkey configured on the server",
    ),
    authorization: Optional[str] = Header(
        default=None,
        description="Bearer token fallback",
    ),
) -> str:
    """Validate administrative credentials using constant-time string comparison."""
    token: Optional[str] = x_admin_key if isinstance(x_admin_key, str) else None

    if not token and isinstance(authorization, str):
        parts = authorization.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1].strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing administrative authorization key. Provide 'X-Admin-Key' header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Constant-time comparison prevents timing attacks
    is_valid = secrets.compare_digest(
        token.encode("utf-8"),
        settings.ADMIN_API_KEY.encode("utf-8"),
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid administrative passkey.",
        )

    return token
