from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import FaceRecognitionException
from app.core.logger import logger

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(FaceRecognitionException)
    async def application_exception_handler(
            request: Request,
            exc: FaceRecognitionException
    ):
        logger.error(exc.message)

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
            request: Request,
            exc: Exception
    ):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "InternalServerError",
                    "message": "Internal Server Error"
                }
            }
        )