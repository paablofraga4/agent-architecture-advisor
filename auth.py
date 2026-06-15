"""Supabase-backed authentication, roles and run-quota for the FastAPI layer.

How it works
------------
- The Next.js frontend logs the user in with Supabase Auth and sends the
  Supabase access token (a JWT) as `Authorization: Bearer <token>`.
- We verify that JWT locally with the project's JWT secret (HS256) — no network
  round-trip per request.
- User role and run quota live in a `profiles` table (see
  supabase/migrations/0001_init.sql). We read/update it through PostgREST using
  the service-role key, which bypasses RLS for these trusted server operations.

Quota model
-----------
- Every new user gets `run_limit = 1` (one free run) via a DB trigger.
- `role = 'admin'` users are unlimited.
- A run is only counted (runs_used += 1) when it finishes successfully.

Required environment variables
------------------------------
  SUPABASE_URL                 https://<project>.supabase.co
  SUPABASE_JWT_SECRET          Project Settings > API > JWT Secret
  SUPABASE_SERVICE_ROLE_KEY    Project Settings > API > service_role key (secret!)

If these are unset we run in OPEN mode (no auth) so local dev / tests keep
working exactly as before. Production MUST set them.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import httpx
import jwt
from fastapi import Depends, Header, HTTPException, status

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

AUTH_ENABLED = bool(SUPABASE_URL and SUPABASE_JWT_SECRET and SUPABASE_SERVICE_ROLE_KEY)

# A synthetic profile used when auth is disabled (local dev / CI). Unlimited so
# nothing breaks; never used in production where AUTH_ENABLED is True.
_DEV_PROFILE = {
    "id": "dev-local",
    "email": "dev@local",
    "role": "admin",
    "run_limit": 10_000_000,
    "runs_used": 0,
}


@dataclass
class CurrentUser:
    id: str
    email: Optional[str]
    role: str
    run_limit: int
    runs_used: int

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def has_quota(self) -> bool:
        return self.is_admin or self.runs_used < self.run_limit


def _rest_headers() -> dict:
    return {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }


def _decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token: {exc}",
        ) from exc


async def _fetch_profile(user_id: str) -> Optional[dict]:
    url = f"{SUPABASE_URL}/rest/v1/profiles"
    params = {"id": f"eq.{user_id}", "select": "*"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, headers=_rest_headers(), params=params)
        r.raise_for_status()
        rows = r.json()
    return rows[0] if rows else None


async def _ensure_profile(user_id: str, email: Optional[str]) -> dict:
    """Read the profile; create a default one if the trigger hasn't (race-safe)."""
    profile = await _fetch_profile(user_id)
    if profile:
        return profile
    url = f"{SUPABASE_URL}/rest/v1/profiles"
    payload = {"id": user_id, "email": email, "role": "user", "run_limit": 1, "runs_used": 0}
    headers = {**_rest_headers(), "Prefer": "resolution=merge-duplicates,return=representation"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        rows = r.json()
    return rows[0] if isinstance(rows, list) and rows else payload


async def increment_runs_used(user_id: str) -> None:
    """Atomically bump runs_used via the SQL function (see migration)."""
    if not AUTH_ENABLED:
        return
    url = f"{SUPABASE_URL}/rest/v1/rpc/increment_runs_used"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, headers=_rest_headers(), json={"p_user_id": user_id})
        r.raise_for_status()


async def get_current_user(
    authorization: Optional[str] = Header(default=None),
) -> CurrentUser:
    """FastAPI dependency: resolve the authenticated user + their quota."""
    if not AUTH_ENABLED:
        return CurrentUser(**_DEV_PROFILE)

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )
    token = authorization.split(" ", 1)[1].strip()
    claims = _decode_jwt(token)
    user_id = claims.get("sub")
    email = claims.get("email")
    if not user_id:
        raise HTTPException(status_code=401, detail="token has no subject")

    profile = await _ensure_profile(user_id, email)
    return CurrentUser(
        id=user_id,
        email=profile.get("email") or email,
        role=profile.get("role", "user"),
        run_limit=int(profile.get("run_limit", 1)),
        runs_used=int(profile.get("runs_used", 0)),
    )


async def require_run_quota(
    user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Dependency for the run endpoint: 402 when the free run is spent."""
    if not user.has_quota:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "code": "QUOTA_EXCEEDED",
                "message": "Has agotado tu prueba gratuita. Solicita acceso para continuar.",
                "runs_used": user.runs_used,
                "run_limit": user.run_limit,
            },
        )
    return user
