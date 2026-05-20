from fastapi import Header, HTTPException
from backend.utils.jwt_handler import verify_token

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:
        # Expected format: "Bearer <token>"
        token = authorization.split(" ")[1]
    except (IndexError, AttributeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or expired"
        )

    return payload
