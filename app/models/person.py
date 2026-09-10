from pydantic import BaseModel, EmailStr
from typing import Optional

class Person(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None