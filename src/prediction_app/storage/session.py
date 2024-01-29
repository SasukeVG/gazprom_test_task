from contextlib import asynccontextmanager

from aiobotocore.session import get_session, AioSession

from prediction_app.storage.config import s3_client_config


async def get_s3_client():
    session: AioSession = get_session()
    async with session.create_client(
        "s3",
        aws_access_key_id=s3_client_config.ACCESS_KEY,
        aws_secret_access_key=s3_client_config.SECRET_KEY,
        endpoint_url=s3_client_config.ENDPOINT,
        region_name="us-east-1",
    ) as s3_client:
        yield s3_client


get_s3_client_ = asynccontextmanager(get_s3_client)
