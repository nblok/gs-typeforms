from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR = Path(__file__).parent
SQLITE_DATABASE_FILEPATH = Path.joinpath(DIR, "..", "db")
LOCAL_LOG_PATH = Path.joinpath(DIR, "..", "logs")


class BaseConfig(BaseSettings):
    ENV_STATE: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: str | None = None
    DATABASE_FORCE_ROLLBACK: bool = False
    LOG_FILE: str | None = None


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")
    DATABASE_URL: str = f"sqlite:///{SQLITE_DATABASE_FILEPATH}/dev.sqlite"
    LOG_FILE: str = f"{LOCAL_LOG_PATH}/typeforms-dev.log"


class TestConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="TEST_")
    DATABASE_URL: str = f"sqlite:///{SQLITE_DATABASE_FILEPATH}/test.sqlite"
    DATABASE_FORCE_ROLLBACK: bool = True
    LOG_FILE: str = f"{LOCAL_LOG_PATH}/typeforms-test.log"


@lru_cache()
def get_config(env_state: str = "dev") -> DevConfig | ProdConfig | TestConfig:
    configs: dict[str, type[DevConfig | ProdConfig | TestConfig]] = {
        "prod": ProdConfig,
        "dev": DevConfig,
        "test": TestConfig,
    }
    return configs[env_state]()
