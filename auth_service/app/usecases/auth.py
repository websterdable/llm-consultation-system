from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository
from app.schemas.user import UserPublic


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> UserPublic:
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError()
        password_hash = hash_password(password)
        user = await self._user_repo.create(email=email, password_hash=password_hash)
        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        token_data = {"sub": str(user.id), "role": user.role}
        return create_access_token(token_data)

    async def me(self, user_id: int) -> UserPublic:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return UserPublic.model_validate(user)