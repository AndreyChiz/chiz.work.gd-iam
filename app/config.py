from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# import os

# env_vars = {
#     "APP_CONFIG__DATABASE__HOST": "localhost",
#     "APP_CONFIG__DATABASE__PORT": "5432",
#     "APP_CONFIG__DATABASE__NAME": "test_db",
#     "APP_CONFIG__DATABASE__USER": "test_user",
#     "APP_CONFIG__DATABASE__PASSWORD": "secret",
#     "APP_CONFIG__DATABASE__ECHO": "true",
#     "APP_CONFIG__DATABASE__ECHO_POOL": "false",
#     "APP_CONFIG__DATABASE__POOL_SIZE": "5",
#     "APP_CONFIG__DATABASE__MAX_OVERFLOW": "10",
# }

# for key, value in env_vars.items():
#     os.environ[key] = value


class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )
    database: DatabaseConfig


settings = Settings()
