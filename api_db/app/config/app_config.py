import logging
from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings, Field, BaseModel

# TODO log this into a file
LOG = logging.getLogger("api_db")


class ConfigException(BaseException):
    """ Class to handle exception related to configuration """
    pass


class AppConfig(BaseModel):
    """Fixed Application configuration"""
    ALERTING_HOST_FILENAME = "config/alerting_host.yaml"
    TEST_ALERTING_HOST_FILENAME = "../app/config/test_alerting_config.yaml"


class GlobalConfig(BaseSettings):
    """Global configuration"""
    APP_CONFIG: AppConfig = AppConfig()
    ENV_STATE: Optional[str] = Field(None, env="ENV")
    LISTEN_PORT: int = Field(None, env="LISTEN_PORT")

    class Config:
        pass


class DevConfig(GlobalConfig):
    """Development configurations."""

    DB_URI: Optional[str] = Field(None, env="DB_URI")
    ALERTING_HOST_FILE: Optional[str] = "config/alerting_host.yaml"

    class Config:
        env_prefix: str = "DEV_"


class TestConfig(GlobalConfig):
    """Test configuration for Jenkins CI only."""

    DB_URI: Optional[str] = "sqlite:///api_db/tests/test.db"
    ALERTING_HOST_FILE = "api_db/app/config/test_alerting_config.yaml"

    class Config:
        env_prefix: str = "TEST_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class GetConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()

        elif self.env_state == "test":
            return TestConfig()

        raise ConfigException('Missing configuration environment')


@lru_cache()
def get_settings() -> BaseSettings:
    LOG.info("Loading config settings from the environment...")
    conf = GetConfig(GlobalConfig().ENV_STATE)()
    return conf
