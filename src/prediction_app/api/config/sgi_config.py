from pydantic import Field, BaseSettings


class SGIConfig(BaseSettings):
    SSL_ENABLED: bool = Field(env="APP_SSL_ENABLED", default=False)
    HTTP_PROTOCOL: str = Field(env="APP_HTTP_PROTOCOL", default="http")
    HOST: str = Field(env="APP_HOST", default="0.0.0.0")
    PORT: int = Field(env="APP_PORT", default=8080)

    WORKERS_COUNT: int = Field(env="APP_WORKERS_COUNT", default=1)

    AUTO_RELOAD: bool = Field(env="APP_AUTORELOAD", default=True)
    # LOG_LEVEL: str = Field(env="APP_LOG_LEVEL", default="info")

    # ACCESS_LOG: str = Field(env="APP_ACCESSLOG_OUTPUT", default="-")  # "-" is to stdout

    WSGI_APP: str = Field(env="APP_WSGI_APP", default="prediction_app.api.main:app")
    WORKER_CLASS: str = Field(env="APP_WORKER_CLASS", default="uvicorn.workers.UvicornWorker")


sgi_config = SGIConfig()
