from app.services.face_service import FaceService
from app.exceptions import (
    MultipleFaceRecognitionException,
    NoFaceDetectionException
)


class EmbeddingService():

    def __init__(self):
        self.face_services = FaceService()

    def generate_embedding(self, image_path: str):
        faces = self.face_services.detect_faces(image_path)

        if len(faces) == 0:
            raise NoFaceDetectionException('No faces detected')

        if len(faces) > 1:
            raise MultipleFaceRecognitionException('More than one face detected')

        return faces[0].embedding