from pydantic import Field, BaseSettings

class S3Config(BaseSettings):
    ACCESS_KEY: str = Field(..., env="APP_S3_ACCESS_KEY")
    SECRET_KEY: str = Field(..., env="APP_S3_SECRET_KEY")
    ENDPOINT: str = Field("http://minio:9000", env="APP_S3_ENDPOINT")
    BUCKET: str = Field("images", env="APP_S3_BUCKET")


s3_client_config = S3Config()
