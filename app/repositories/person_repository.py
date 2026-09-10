from app.database.mongodb import persons_collection
from bson import ObjectId

class PersonRepository():
    @staticmethod
    def create(person: dict):
        return persons_collection.insert_one(person)

    @staticmethod
    def get_by_id(person_id: str):
        person = persons_collection.find_one({"_id": ObjectId(person_id)})
        if person:
            person["_id"] = str(person["_id"])

        return person

    @staticmethod
    def get_all(skip: int, limit: int):
        return persons_collection.find().skip(skip).limit(limit)

    @staticmethod
    def delete(person_id: str):
        return persons_collection.delete_one({"_id": ObjectId(person_id)})

    @staticmethod
    def total_count():
        return persons_collection.count_documents({})

    @staticmethod
    def update(person_id: str, person: dict):
        return persons_collection.update_one(
            {"_id": ObjectId(person_id)},
            {"$set": person}
        )
