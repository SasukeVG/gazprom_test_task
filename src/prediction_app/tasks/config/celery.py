from pydantic import BaseSettings, Field

from prediction_app.tasks.config.redis import REDIS_AUTH, redis_config


class CeleryConfig(BaseSettings):
    BROKER_URL: str = Field(
        env="CELERY_BROKER_URL",
        default=f"redis://{REDIS_AUTH}{redis_config.HOST}:{redis_config.PORT}/{redis_config.DATABASE}",
    )
    BACKEND_URL: str = Field(
        env="CELERY_BACKEND_URL",
        default=f"redis://{REDIS_AUTH}{redis_config.HOST}:{redis_config.PORT}/{redis_config.DATABASE}",
    )


celery_config = CeleryConfig()
