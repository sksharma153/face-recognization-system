from fastapi import FastAPI
from app.api import recognize, person
from app.core.handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.include_router(person.router)
app.include_router(recognize.router)