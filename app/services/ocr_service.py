import easyocr
import time

class OCRService:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def process_image(self, image_path: str) -> tuple[str, float, float]:
        start_time = time.time()
        results = self.reader.readtext(image_path)
        extracted_text = " ".join([text for (_, text, _) in results])
        confidence = sum([conf for (_, _, conf) in results]) / len(results) if results else 0.0
        processing_time = time.time() - start_time
        return extracted_text, confidence, processing_time