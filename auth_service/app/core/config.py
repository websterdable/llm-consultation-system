from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "auth-service"
    env: str = "local"

    # JWT
    jwt_secret: str = "change_me_super_secret"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    # SQLite
    sqlite_path: str = "./auth.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()