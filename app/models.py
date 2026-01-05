from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    confidence: float
    processing_time: float

class ErrorResponse(BaseModel):
    error: str
    detail: str

class ImageUploadResponse(BaseModel):
    image_id: str

class AnalyzeRequest(BaseModel):
    image_id: str

class AnalysisResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: list[str]
    confidence: float