import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from prediction_app.db.connector import get_db_connection_
from prediction_app.db.model import insert_info_prediction_table
from prediction_app.storage.config import s3_client_config
from prediction_app.storage.session import get_s3_client
from prediction_app.tasks.task import testing_task

router = APIRouter(
    prefix='/image_classification_model',
    tags=['Image Classification Model'],
)


@router.post('/predict')
async def inference_by_image(
    image: UploadFile = File(..., media_type='image/*'),
    s3_client=Depends(get_s3_client),
    db_connection=Depends(get_db_connection_),
) -> uuid.UUID:
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    id_ = uuid.uuid4()
    await insert_info_prediction_table(db_connection, id_)

    content = await image.read()
    await s3_client.put_object(Bucket=s3_client_config.BUCKET, Key=str(id_), Body=content)

    await testing_task.delay(
        id_=id_
    )

    return id_
