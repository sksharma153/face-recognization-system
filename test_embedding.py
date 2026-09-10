from app.services.embedding_service import EmbeddingService

service = EmbeddingService()
embedding = service.generate_embedding('app/storage/images/Sandeep.jpg')

print(type(embedding))
print(len(embedding))