'''from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.exceptions import (
    NoFaceDetectionException, MultipleFaceRecognitionException
)
from app.services.person_service import PersonService

router = APIRouter()
person_service = PersonService()

@router.post("/persons")
async def register_person(
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        address: str = Form(None),
        image: UploadFile = File(...)
):
    try:
        person_id = person_service.register_person(
            name,
            email,
            phone,
            address,
            image
        )
        return {
            "message": "person registered successfully",
            "person_id": person_id
        }

    except NoFaceDetectionException as e:
        raise HTTPException(status_code=400, detail=str(e))

    except MultipleFaceRecognitionException as e:
        raise HTTPException(status_code=400, detail=str(e))

'''

