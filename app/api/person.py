from fastapi import APIRouter, UploadFile, File, Form
from fastapi.params import Query

from app.schemas.person import (
    PersonResponse,
    PersonDetailsResponse,
    PersonListResponse,
    UpdatePersonResponse,
    UpdatePersonRequest, AddImageInfoResponse, DeletePersonResponse
)
from app.services.person_service import PersonService

router = APIRouter(
    prefix="/persons",
    tags=["Persons"]
)

person_service = PersonService()

@router.post("", response_model=PersonResponse)
async def register_person(
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        address: str = Form(None),
        image: UploadFile = File(...)
):
    person_id =  person_service.register_person(
        name=name,
        email=email,
        phone=phone,
        address=address,
        image=image
    )
    return PersonResponse(
        message= "Person registered successfully",
        person_id= person_id
    )

@router.get("/{person_id}", response_model=PersonDetailsResponse)
async def get_person(person_id: str):
    return person_service.get_person(person_id)

@router.get("", response_model=PersonListResponse)
async def get_all_persons(
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=1, le=100),
):
    return person_service.get_all_persons(page, size)

@router.put("/{person_id}", response_model=UpdatePersonResponse)
async def update_person(person_id: str, person: UpdatePersonRequest):
    return person_service.update_person(person_id, person)

@router.delete("/{person_id}", response_model=DeletePersonResponse)
async def delete_person(person_id: str):
    return person_service.delete_person(person_id)

@router.post("/{person_id}/images", response_model=AddImageInfoResponse)
async def add_image_info(person_id: str, image: UploadFile = File(...)):
    return person_service.add_person_image(person_id, image)