import logging

import restate
import structlog
from googleapiclient.discovery import build
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .restate_youtube import Executor, create_service


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")  # pyright: ignore[reportUnannotatedClassAttribute]

    google_api_key: str

    service_name: str = "YouTube"

    identity_keys: list[str] = Field(alias="restate_identity_keys", default=[])


settings = Settings()  # pyright: ignore[reportCallIssue]

# logging.basicConfig(level=logging.INFO)
structlog.stdlib.recreate_defaults(log_level=logging.INFO)


executor = Executor(
    build("youtube", "v3", developerKey=settings.google_api_key),
    logger=structlog.get_logger("elevenlabs"),
)

service = create_service(
    executor,
    service_name=settings.service_name,
)

app = restate.app(services=[service], identity_keys=settings.identity_keys)
