from fastapi import FastAPI
from app.api.routes import model_router
from container import ApplicationContainer 
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = ApplicationContainer()
    app.container = container
    app.container.wire(modules=['app.api.handler'])
    app.container.init_resources()
    yield
    app.container.shutdown_resources()


app = FastAPI(lifespan=lifespan)

app.include_router(model_router)