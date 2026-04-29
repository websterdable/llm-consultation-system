from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "bot-service"
    env: str = "local"

    telegram_bot_token: str = ""
    jwt_secret: str = "change_me_super_secret"
    jwt_alg: str = "HS256"

    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "nvidia/nemotron-3-super-120b-a12b:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "bot-service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()