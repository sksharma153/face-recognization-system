import numpy as np

from app.services.faiss_services import FaissService

faiss_services = FaissService()

embedding = np.random.rand(512).astype(np.float32)

index = faiss_services.add_embedding(embedding)

print(index)

distances, index = faiss_services.search(embedding)

print(distances)
print(index)