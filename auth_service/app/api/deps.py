from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(session)


async def get_auth_uc(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()
        return int(user_id)
    except JWTError:
        raise InvalidTokenError()