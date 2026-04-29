from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(
    request: RegisterRequest,
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
):
    return await auth_uc.register(request.email, request.password)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
):
    token = await auth_uc.login(form.username, form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
):
    return await auth_uc.me(user_id)