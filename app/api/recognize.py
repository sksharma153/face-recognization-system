from fastapi import APIRouter, File, UploadFile

from app.services.recognition_service import RecognitionService

router = APIRouter()

@router.post("/recognize")
async def recognize(image: UploadFile = File(...)):
    recognition_service = RecognitionService()
    return recognition_service.recognize(image)