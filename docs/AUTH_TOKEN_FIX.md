# BenchGoblins — Token Expiry Fix & Auth Strategy

## The Problem

**"Token has expired"** = your JWT's `exp` claim is in the past when the backend validates it.

The retry button reuses the same dead token → fails again. Users are stuck.

---

## Fix 1: Backend — Proper JWT Auth (FastAPI)

```python
# src/auth/dependencies.py
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # never hardcode
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60        # 1 hour — reasonable for a web app
REFRESH_TOKEN_EXPIRE_DAYS = 30          # long-lived refresh token

security = HTTPBearer()


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload["sub"]
    except ExpiredSignatureError:
        # Return a specific code the frontend can act on
        raise HTTPException(
            status_code=401,
            detail="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

```python
# src/auth/routes.py
from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt, ExpiredSignatureError
from .dependencies import (
    SECRET_KEY, ALGORITHM, create_access_token, create_refresh_token
)
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest):
    """Exchange a valid refresh token for a new access + refresh token pair."""
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired — please log in again")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),  # rotate the refresh token too
    )


@router.post("/login", response_model=TokenResponse)
async def login(/* your existing login logic */):
    # After validating credentials:
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )
```

**Why rotate the refresh token?** If a refresh token leaks, rotating on use means the attacker's copy stops working the moment the real user refreshes. It's called **refresh token rotation** — it's the current industry standard.

---

## Fix 2: Frontend — Axios Interceptor (auto-refresh)

This is the real fix for the UX problem. Instead of showing an error, the frontend silently refreshes and retries.

```typescript
// src/lib/apiClient.ts
import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "https://api.benchgoblins.com";

// Storage helpers — abstract so you can swap localStorage ↔ secure cookie later
const getAccessToken = () => localStorage.getItem("access_token");
const getRefreshToken = () => localStorage.getItem("refresh_token");
const setTokens = (access: string, refresh: string) => {
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
};
const clearTokens = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

const api: AxiosInstance = axios.create({ baseURL: BASE_URL });

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// --- The critical piece ---
let isRefreshing = false;
let refreshQueue: Array<(token: string) => void> = [];

const processQueue = (newToken: string) => {
  refreshQueue.forEach((resolve) => resolve(newToken));
  refreshQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config as AxiosRequestConfig & { _retried?: boolean };

    const isExpired =
      error.response?.status === 401 &&
      error.response?.data?.detail === "TOKEN_EXPIRED" &&
      !original._retried; // prevent infinite retry loops

    if (!isExpired) return Promise.reject(error);

    // If a refresh is already in flight, queue this request
    if (isRefreshing) {
      return new Promise((resolve) => {
        refreshQueue.push((token) => {
          original.headers = { ...original.headers, Authorization: `Bearer ${token}` };
          resolve(api(original));
        });
      });
    }

    original._retried = true;
    isRefreshing = true;

    try {
      const { data } = await axios.post(`${BASE_URL}/auth/refresh`, {
        refresh_token: getRefreshToken(),
      });

      setTokens(data.access_token, data.refresh_token);
      processQueue(data.access_token);

      // Retry the original request with new token
      original.headers = {
        ...original.headers,
        Authorization: `Bearer ${data.access_token}`,
      };
      return api(original);
    } catch (refreshError) {
      // Refresh token itself is expired — force logout
      clearTokens();
      refreshQueue = [];
      window.location.href = "/login?reason=session_expired";
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
```

**The queue pattern matters:** If 3 requests fire simultaneously and all get 401, you only want ONE refresh call, not three racing each other. The queue holds the others until the refresh completes, then retries them all with the new token.

---

## Fix 3: The "Retry" Button (immediate patch)

If you can't ship the interceptor today, at minimum fix the retry so it refreshes first:

```typescript
// In your error component
const handleRetry = async () => {
  try {
    // Try to refresh before retrying the original request
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
      const { data } = await axios.post("/auth/refresh", { refresh_token: refreshToken });
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
    }
    // Now retry the original action
    await originalAction();
  } catch {
    // Refresh failed — send to login
    router.push("/login?reason=session_expired");
  }
};
```

---

## Optimal Pattern: Silent Proactive Refresh

Even better than reactive refresh (after a 401) is **proactive refresh** — refresh before the token expires.

```typescript
// src/lib/tokenManager.ts
const REFRESH_BUFFER_SECONDS = 60; // refresh 60s before expiry

function getTokenExpiry(token: string): number {
  const payload = JSON.parse(atob(token.split(".")[1]));
  return payload.exp * 1000; // convert to ms
}

function scheduleRefresh() {
  const token = getAccessToken();
  if (!token) return;

  const expiry = getTokenExpiry(token);
  const now = Date.now();
  const refreshAt = expiry - REFRESH_BUFFER_SECONDS * 1000;
  const delay = refreshAt - now;

  if (delay <= 0) {
    // Already expired or about to — refresh immediately
    doRefresh();
    return;
  }

  setTimeout(async () => {
    await doRefresh();
    scheduleRefresh(); // reschedule for the new token
  }, delay);
}

async function doRefresh() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return;
  try {
    const { data } = await axios.post("/auth/refresh", { refresh_token: refreshToken });
    setTokens(data.access_token, data.refresh_token);
  } catch {
    clearTokens();
    window.location.href = "/login?reason=session_expired";
  }
}

// Call on app boot and after login
export { scheduleRefresh };
```

Users **never** see a token error. The token is always fresh.

---

## Summary: What to Ship and When

| Priority | Fix | Effort | Impact |
|----------|-----|--------|--------|
| **Now** | Fix Retry button to refresh first | 30 min | Stops the bleeding |
| **This week** | Axios interceptor (reactive refresh) | 2–3 hrs | Users never see the error |
| **Next sprint** | Refresh token rotation on backend | 2 hrs | Security best practice |
| **Later** | Proactive token refresh scheduler | 2 hrs | Zero-friction sessions |

---

## Security Notes

- Store refresh tokens in **httpOnly cookies** if you can — localStorage is XSS-vulnerable. This requires a backend cookie endpoint but is significantly more secure.
- **Never** store tokens in `sessionStorage` (same XSS risk, worse UX).
- Set `Secure` and `SameSite=Strict` on any auth cookies.
- Add a token **revocation list** (Redis or DB) if you ever need to force-logout a user (e.g., password change, account compromise).
