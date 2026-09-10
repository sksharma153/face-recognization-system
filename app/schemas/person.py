from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]

class PersonSummary(BaseModel):
    id: str
    name: str
    email: str

class PersonListResponse(BaseModel):
    persons: list[PersonSummary]
    total: int
    page: int
    size: int
    total_pages: int

class PersonResponse(BaseModel):
    message: str
    person_id: str

class ImageInfo(BaseModel):
    image_path: str
    faiss_index: int
    created_at: datetime

class PersonDetailsResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]
    images: list[ImageInfo]

class UpdatePersonRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]

class UpdatePersonResponse(BaseModel):
    message: str

class DeletePersonResponse(BaseModel):
    message: str

class AddImageInfoResponse(BaseModel):
    message: str
