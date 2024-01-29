from fastapi import FastAPI

from prediction_app.api.inference_router import router as inference_router
from prediction_app.api.lifespan import lifespan
from prediction_app.api.prediction_router import router as prediction_router
from prediction_app.api.prediction_router import predictions_router as predictions_router

app = FastAPI(lifespan=lifespan)

app.include_router(inference_router)
app.include_router(prediction_router)
app.include_router(predictions_router)

