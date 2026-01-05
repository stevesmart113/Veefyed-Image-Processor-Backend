import os
import uuid
from PIL import Image
import io

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_image(contents: bytes) -> bool:
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        return True
    except Exception:
        return False

def validate_file_size(contents: bytes) -> bool:
    return len(contents) <= MAX_FILE_SIZE

def save_temp_file(contents: bytes, filename: str) -> str:
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)
    return temp_path

def save_upload_file(contents: bytes, filename: str) -> str:
    image_id = str(uuid.uuid4())
    ext = os.path.splitext(filename)[1]
    filepath = f"uploads/{image_id}{ext}"
    with open(filepath, "wb") as f:
        f.write(contents)
    return image_id

def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)