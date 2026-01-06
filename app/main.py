import logging
from fastapi import FastAPI # type: ignore
from app.routes.upload import router as upload_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Veefyed Backend", description="A FastAPI backend for Veefyed", version="1.0.0")

app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Veefyed Backend"}