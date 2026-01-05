from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models import UploadResponse, ImageUploadResponse, AnalyzeRequest, AnalysisResponse
from app.services.ocr_service import OCRService
from app.utils.file_utils import validate_image, validate_file_size, save_temp_file, save_upload_file, cleanup_temp_file
import random
import os
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

router = APIRouter()
ocr_service = OCRService()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    logger.info(f"Image upload started for file: {file.filename}")

    try:
        if not file.filename:
            logger.warning("Upload failed: No file provided")
            raise HTTPException(status_code=400, detail="No file provided")

        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            logger.warning(f"Upload failed: Invalid file type {file.content_type}")
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG allowed.")

        # Read file content
        contents = await file.read()

        # Validate file size
        if not validate_file_size(contents):
            logger.warning(f"Upload failed: File too large ({len(contents)} bytes)")
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB.")

        # Validate image
        if not validate_image(contents):
            logger.warning("Upload failed: Invalid image file")
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Save file and get image_id
        image_id = save_upload_file(contents, file.filename)
        logger.info(f"Image uploaded successfully with ID: {image_id}")

        return ImageUploadResponse(image_id=image_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(request: AnalyzeRequest):
    image_id = request.image_id
    logger.info(f"Analysis started for image_id: {image_id}")

    try:
        if not image_id or not image_id.strip():
            logger.warning("Analysis failed: image_id is required and cannot be empty")
            raise HTTPException(status_code=400, detail="image_id is required and cannot be empty")

        # Check if image exists
        uploads_dir = "uploads"
        if not os.path.exists(uploads_dir):
            logger.warning("Analysis failed: uploads directory not found")
            raise HTTPException(status_code=404, detail="Image not found")

        # Check if any file starts with image_id
        found = False
        for filename in os.listdir(uploads_dir):
            if filename.startswith(image_id):
                found = True
                break

        if not found:
            logger.warning(f"Analysis failed: Image not found for image_id {image_id}")
            raise HTTPException(status_code=404, detail="Image not found for the given image_id")

        # Mock analysis logic
        skin_types = ["Dry", "Oily", "Combination", "Normal"]
        possible_issues = ["Hyperpigmentation", "Acne", "Wrinkles", "Redness", "Dryness"]

        # Use hash of image_id for deterministic but varied results
        hash_val = hash(image_id)
        skin_type = skin_types[hash_val % len(skin_types)]

        # Generate 0-2 issues
        num_issues = (hash_val // len(skin_types)) % 3
        issues = random.sample(possible_issues, num_issues)

        # Confidence between 0.7 and 0.95
        confidence = 0.7 + (hash_val % 26) / 100

        result = AnalysisResponse(
            image_id=image_id,
            skin_type=skin_type,
            issues=issues,
            confidence=round(confidence, 2)
        )

        logger.info(f"Analysis completed for image_id {image_id}: skin_type={skin_type}, issues={issues}, confidence={result.confidence}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis for image_id {image_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# @router.post("/upload-image", response_model=UploadResponse)
# async def upload_image_ocr(file: UploadFile = File(...)):
#     logger.info(f"OCR upload started for file: {file.filename}")

#     try:
#         if not file.filename:
#             logger.warning("OCR upload failed: No file provided")
#             raise HTTPException(status_code=400, detail="No file provided")

#         # Validate file type
#         allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
#         if file.content_type not in allowed_types:
#             logger.warning(f"OCR upload failed: Invalid file type {file.content_type}")
#             raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG allowed.")

#         # Read file content
#         contents = await file.read()

#         # Validate with PIL
#         if not validate_image(contents):
#             logger.warning("OCR upload failed: Invalid image file")
#             raise HTTPException(status_code=400, detail="Invalid image file")

#         # Save to temp file
#         temp_path = save_temp_file(contents, file.filename)

#         try:
#             # Process with OCR
#             extracted_text, confidence, processing_time = ocr_service.process_image(temp_path)

#             result = UploadResponse(
#                 filename=file.filename,
#                 extracted_text=extracted_text,
#                 confidence=confidence,
#                 processing_time=processing_time
#             )

#             logger.info(f"OCR processing completed for {file.filename}: extracted {len(extracted_text)} characters in {processing_time:.2f}s")
#             return result
#         finally:
#             # Cleanup
#             cleanup_temp_file(temp_path)
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error during OCR upload: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")