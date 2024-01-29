from pydantic import Field, BaseSettings


class DatabaseConfig(BaseSettings):
    USER: str = Field(..., env="POSTGRES_USER")
    PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    HOST: str = Field('postgres', env="POSTGRES_HOST")
    PORT: int = Field(5432, env="POSTGRES_PORT")
    DB_NAME: str = Field("postgres_db", env="POSTGRES_DB_NAME")


database_config = DatabaseConfig()
