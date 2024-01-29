import io
from time import perf_counter

import numpy as np
from PIL import Image

from prediction_app.db.connector import get_db_connection
from prediction_app.db.model import update_info_prediction_table
from prediction_app.domain.custom_inference import bootstrap, forward
from prediction_app.storage.config import s3_client_config
from prediction_app.storage.session import get_s3_client_
from prediction_app.tasks.main import celery_app


#

async def get_file_from_s3(s3_client, id_):
    response = await s3_client.get_object(Bucket=s3_client_config.BUCKET, Key=str(id_))
    content = await response['Body'].read()
    return content


@celery_app.task(name='testing_task')
async def testing_task(*args, **kwargs):
    id_ = kwargs.get('id_')

    async with get_s3_client_() as s3_client:
        content = await get_file_from_s3(s3_client, id_)
        print(len(content))

    pil_image = Image.open(io.BytesIO(content)).convert('RGB').resize((112, 112))

    numpy_image = np.array(pil_image).reshape((1, 112, 112, 3)).astype("float32") / 255.0
    print(numpy_image.shape)

    model = {}
    model_wb = np.load('/opt/app-root/ds/SFDDD_model.npz')
    model["conv_weights"] = model_wb['conv_weights'].astype("float32")
    model["conv_biases"] = model_wb['conv_biases'].astype("float32")
    model["dense_weights"] = model_wb['dense_weights'].astype("float32")
    model["dense_biases"] = model_wb['dense_biases'].astype("float32")

    start = perf_counter()
    bootstrap()
    print(f'bootstrap: {perf_counter() - start:.2f}')

    predictions = forward(numpy_image, model["conv_weights"], model["conv_biases"], model["dense_weights"], model["dense_biases"])
    predicted_class = np.argmax(predictions, axis=1).tolist()[0]
    predicted_probability = np.max(predictions, axis=1).tolist()[0]

    async with get_db_connection() as db_connection:
        await update_info_prediction_table(db_connection, id_, predicted_class, predicted_probability)


