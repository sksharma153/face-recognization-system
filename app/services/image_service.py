import os
import tempfile
import uuid
import shutil
from fastapi import UploadFile

from app.core.config import settings
from app.core.logger import logger


class ImageService():

    IMAGE_DIR = settings.IMAGE_DIRECTORY

    @classmethod
    def save_image(cls, image: UploadFile) -> str:
        os.makedirs(cls.IMAGE_DIR, exist_ok=True)

        extension = image.filename.split(".")[-1]

        filename = f"{uuid.uuid4()}.{extension}"

        image_path = os.path.join(cls.IMAGE_DIR, filename)

        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        return image_path

    @staticmethod
    def save_temp_image(image: UploadFile) -> str:
        extension = image.filename.split(".")[-1]

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{extension}"
        )

        shutil.copyfileobj(image.file, temp)
        temp.close()
        return temp.name

    @staticmethod
    def delete_image(path: str) :
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            logger.exception("Failed to delete image", path)
