from typing import Optional
from fastapi import Header, HTTPException, status
from shared.models import User

async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> User:
    """Very small authentication dependency for local/dev use.

    - If `X-User-Id` header is provided, return that user id.
    - If `Authorization: Bearer user:<id>` is provided, extract id.
    - Otherwise raise 401.

    NOTE: This is a stub for development. Replace with real JWT verification in production.
    """
    uid = None
    if x_user_id:
        try:
            uid = int(x_user_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-User-Id header")
    elif authorization and authorization.startswith("Bearer "):
        token = authorization[len("Bearer "):]
        # accept a simple bearer token format: "user:<id>" for local testing
        if token.startswith("user:"):
            try:
                uid = int(token.split(":", 1)[1])
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bearer token format")
    
    if uid is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # Minimal user object -- other fields can be populated by user service in production
    return User(id=uid, email=f"user{uid}@example.com", username=f"user{uid}")

# Re-export User model for convenience
User = User
