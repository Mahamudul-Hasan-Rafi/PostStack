from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Configuration settings for the application."""

    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database configuration
    # db_url: str = Field(..., env="DATABASE_URL", description="Database connection URL")


class GlobalConfig(BaseConfig):
    """Global configuration settings for the application."""

    # Additional global settings can be added here
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    """Development configuration settings for the application."""

    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    """Test configuration settings for the application."""

    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_", env_file_encoding="utf-8")


def get_config(env) -> BaseConfig:
    """Get the appropriate configuration based on the environment."""
    env_state = env.lower() if env else "global"

    if env_state == "dev":
        return DevConfig()
    elif env_state == "test":
        return TestConfig()
    else:
        return GlobalConfig()


print("Loading configuration...")
print(f"Environment State: {BaseConfig().ENV_STATE}")
config = get_config(BaseConfig().ENV_STATE)
