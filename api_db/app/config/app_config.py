import logging
import os

from pydantic import BaseSettings

# TODO log this into a file
log = logging.getLogger("api_db")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 1)
    environment_endpoint_active: bool = os.getenv("ENV_ENDPOINT_ACTIVE", 0)


def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
