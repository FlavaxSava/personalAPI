from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    github_username: str
    github_token: SecretStr


settings = Settings()  # type: ignore[call-arg]
