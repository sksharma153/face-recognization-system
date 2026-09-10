from datetime import datetime

from starlette.datastructures import UploadFile

from app.core.exceptions import FaceNotDetectedException, PersonNotFoundException
from app.core.logger import logger
from app.repositories.person_repository import PersonRepository
from app.repositories.embedding_repository import EmbeddingRepository
from app.schemas.person import ImageInfo, PersonDetailsResponse, PersonSummary, PersonListResponse, UpdatePersonRequest, \
    UpdatePersonResponse, DeletePersonResponse, AddImageInfoResponse
from app.services.image_service import ImageService
from app.services.embedding_service import EmbeddingService
from app.services.faiss_services import FaissService
import math

class PersonService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.faiss_service = FaissService()

    def _save_person_image(self, person_id: str, image: UploadFile) -> dict:
        image_path = ImageService.save_image(image)
        try:
            embedding = self.embedding.generate_embedding(image_path)
            if embedding is None:
                raise FaceNotDetectedException(
                    "No face detected is the uploaded image."
                )
            faiss_index = self.faiss_service.add_embedding(embedding)

            return {
                "person_id": person_id,
                "image_path": image_path,
                "embedding": embedding,
                "faiss_index": faiss_index
            }
        except Exception:
            ImageService.delete_image(image_path)
            raise

    def _save_embedding_metadata(self, person_id: str, image_details: dict) :
        EmbeddingRepository.create_embedding({
            "person_id": person_id,
            "faiss_index": image_details["faiss_index"],
            "image_path": image_details["image_path"],
            "created_at": datetime.utcnow(),
            "embedding": image_details["embedding"].tolist(),
        })

    def _normalize_person(self, person) -> dict:
        return {
            "id": str(person["_id"]),
            "name": person["name"],
            "email": person["email"],
            "phone": person["phone"],
            "address": person.get("address"),
        }

    def _rebuild_faiss_index(self):
        embedding_doc = EmbeddingRepository.get_all()
        vector = [
            doc["embedding"]
            for doc in embedding_doc
        ]
        self.faiss_service.rebuild_index(vector)

    def register_person(
            self,
            name,
            email,
            phone,
            address,
            image
    ) -> str:
        logger.info("========== START REGISTER ==========")

        person = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }

        result = PersonRepository.create(person)
        person_id = str(result.inserted_id)

        image_details = self._save_person_image(person_id, image)

        self._save_embedding_metadata(person_id, image_details)

        logger.info("========== END REGISTER ==========")
        return person_id

    def get_person(self, person_id: str) -> PersonDetailsResponse:
        person = PersonRepository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundException(
                "No person was found with the given ID."
            )

        person = self._normalize_person(person)

        embeddings = EmbeddingRepository.find_by_person(person_id)

        images = [
            ImageInfo(
                image_path=embedding["image_path"],
                faiss_index=embedding["faiss_index"],
                created_at=embedding["created_at"]
            )
            for embedding in embeddings
        ]
        return PersonDetailsResponse(
            id=person["id"],
            name=person["name"],
            email=person["email"],
            phone=person["phone"],
            address=person["address"],
            images=images
        )

    def get_all_persons(self, page: int, size: int) -> PersonListResponse:
        skip = (page - 1) * size
        limit = size
        persons = PersonRepository.get_all(skip, limit)
        count = PersonRepository.total_count()

        person_summaries = []
        for person in persons:
            normalized = self._normalize_person(person)
            person_summaries.append(
                PersonSummary(
                    id=normalized["id"],
                    name=normalized["name"],
                    email=normalized["email"],
                )
            )

        return PersonListResponse(
            persons = person_summaries,
            total=count,
            total_pages=math.ceil(count / size),
            page=page,
            size=size,
        )

    def update_person(self, person_id: str, request: UpdatePersonRequest) -> UpdatePersonResponse:
        person = PersonRepository.get_by_id(person_id)
        if person is None:
            raise PersonNotFoundException(
                "No person was found with the given ID."
            )

        update_data = request.model_dump()
        logger.info("Updating person: %s", person_id)
        PersonRepository.update(person_id, update_data)

        return UpdatePersonResponse(
            message="Person updated successfully.",
        )

    def delete_person(self, person_id: str) -> DeletePersonResponse:
        person = PersonRepository.get_by_id(person_id)

        if person is None:
            raise PersonNotFoundException("No person was found with the given ID.")

        embeddings = EmbeddingRepository.find_by_person(person_id)

        for embedding in embeddings:
            ImageService.delete_image(embedding["image_path"])

        EmbeddingRepository.delete_by_person(person_id)
        PersonRepository.delete(person_id)
        self._rebuild_faiss_index()

        return DeletePersonResponse(
            message = "Person deleted successfully."
        )

    def add_person_image(self, person_id: str, image: UploadFile) -> AddImageInfoResponse:
        image_details = self._save_person_image(person_id, image)
        self._save_embedding_metadata(person_id, image_details)

        return AddImageInfoResponse(
            message="Person image added successfully."
        )








