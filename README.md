# Veefyed Backend

A FastAPI backend for the Veefyed application.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   Note: EasyOCR may require additional system dependencies. On macOS, you might need to install torch separately if issues arise.

## Running the Application

### Using Virtual Environment
Activate the virtual environment and run the server:
```
source venv/bin/activate
uvicorn app.main:app --reload
```

### Using Docker
Build and run with Docker:
```
docker build -t veefyed-backend .
docker run -p 8000:8000 veefyed-backend
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once running, visit `http://127.0.0.1:8000/docs` for interactive API documentation provided by Swagger UI.

## Endpoints
- `POST /upload` - Upload an image and get image_id
  - Accepts: multipart/form-data with 'file' field
  - Use form-data in uploading the image on postman. The image file can be selected from there.
  - Supported formats: JPEG, PNG
  - Max size: 5MB
  - Returns: JSON with generated image_id
- `POST /analyze` - Analyze an uploaded image
  - Accepts: JSON with 'image_id' field as a body request
  - Returns: JSON with skin_type, issues, and confidence score
  - Errors: 400 for missing image_id, 404 for unknown image_id
