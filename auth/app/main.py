from fastapi import FastAPI
from auth.app.api.v1.auth import router as auth_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

Instrumentator().instrument(app).expose(app)