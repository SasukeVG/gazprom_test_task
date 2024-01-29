from pydantic import BaseSettings, Field


class RedisConfig(BaseSettings):
    HOST: str = Field(
        env="REDIS_HOST",
        default="redis",
    )
    PORT: int = Field(
        env="REDIS_PORT",
        default=6379,
    )
    PASSWORD: str = Field(
        env="REDIS_PASSWORD",
        default="",
    )
    DATABASE: int = Field(
        env="REDIS_DATABASE",
        default=0,
    )


redis_config = RedisConfig()
REDIS_AUTH: str = f':{redis_config.PASSWORD}@' if redis_config.PASSWORD.strip() != '' else ''
