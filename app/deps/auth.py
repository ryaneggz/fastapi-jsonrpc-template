from typing import Optional
from fastapi import Header, HTTPException, status
from pydantic import BaseModel

class AuthContext(BaseModel):
    user_id: Optional[str] = None
    scopes: list[str] = []

async def auth_dependency(authorization: Optional[str] = Header(None)) -> AuthContext:
    # Replace with real verification
    if authorization is None:
        return AuthContext(user_id=None, scopes=[])
    if authorization != "Bearer devtoken":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return AuthContext(user_id="dev", scopes=["rpc:all"])
