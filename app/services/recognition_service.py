from app.core.config import settings
from app.core.exceptions import FaceRecognitionException
from app.repositories.embedding_repository import EmbeddingRepository
from app.repositories.person_repository import PersonRepository
from app.services.embedding_service import EmbeddingService
from app.services.faiss_services import FaissService
from app.services.image_service import ImageService


class RecognitionService:

    def __init__(self):
        self.embedding_services = EmbeddingService()

    def recognize(self, image_path: str):
        temp_image = None

        try:
            faiss_services = FaissService()
            temp_image = ImageService.save_image(image_path)

            embedding = self.embedding_services.generate_embedding(temp_image)

            if embedding is None:
                raise FaceRecognitionException(
                    "Not able to recognize the image."
                )

            faiss_record = faiss_services.search(embedding)

            if faiss_record['score'] < settings.MATCH_THRESHOLD:
                return {
                    "matched": False,
                    "confidence": float(faiss_record['score']),
                    "person": None,
                    "message": "Unknown person"
                }

            metadata = EmbeddingRepository.find_by_faiss_index(faiss_record['index'])

            if metadata is None:
                return {
                    "matched": False,
                    "confidence": float(faiss_record['score']),
                    "person": None,
                    "message": "Embedding metadata not found"
                }

            person = PersonRepository.get_by_id(metadata["person_id"])

            if person is None:
                return {
                    "matched": False,
                    "confidence": float(faiss_record['score']),
                    "person": None,
                    "message": "Person not found"
                }

            return {
                "matched": True,
                "confidence": float(faiss_record['score']),
                "person": person,
                "message": None
            }

        finally:
            if temp_image:
                ImageService.delete_image(temp_image)