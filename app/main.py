from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="S3 Proxy Service")

app.include_router(router)
