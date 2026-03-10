from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    celery_broker_url: str
    celery_result_backend: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
