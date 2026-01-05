import logging
from fastapi import FastAPI
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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}