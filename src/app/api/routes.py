from fastapi import APIRouter

from app.api.handler import predict

model_router = APIRouter(prefix='/model')

model_router.add_api_route('/predict', predict)