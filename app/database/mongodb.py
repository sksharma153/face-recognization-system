from pymongo import MongoClient
from dotenv import load_dotenv
import os

from app.core.config import settings

load_dotenv()

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
persons_collection = db["persons"]
embedding_collection = db["embeddings"]
