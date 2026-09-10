from bson import ObjectId
from app.database.mongodb import embedding_collection

class EmbeddingRepository:

    @staticmethod
    def create_embedding(embedding_doc: dict):
        return embedding_collection.insert_one(embedding_doc)

    @staticmethod
    def find_person_by_id(person_id: str):
        return embedding_collection.find_one({"person_id": person_id})

    @staticmethod
    def get_all():
        return list(embedding_collection.find())

    @staticmethod
    def find_by_faiss_index(faiss_index: int):

        docs = list(embedding_collection.find())
        for doc in docs:
            print(doc)

        result = embedding_collection.find_one({
            "faiss_index": int(faiss_index)
        })

        return result

    @staticmethod
    def find_by_person(person_id: str):
        return list(
            embedding_collection.find(
                {"person_id": person_id}
            )
        )

    @staticmethod
    def count_by_person(person_id: str):
        return embedding_collection.count_documents({"person_id": person_id})

    @staticmethod
    def delete_by_person(person_id: str):
        return embedding_collection.delete_many({"person_id": person_id})
