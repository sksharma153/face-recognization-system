import faiss
import numpy as np
import os

from app.core.config import settings
from app.core.logger import logger


class FaissService:

    def __init__(self):

        self.dimension = 512
        os.makedirs("faiss", exist_ok=True)
        index_path = os.path.join(
            settings.FAISS_DIRECTORY,
            settings.FAISS_INDEX_NAME,
        )

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

            if not isinstance(self.index, faiss.IndexFlatIP):
                logger.info("Old FAISS index detected. Recreating")
                os.remove(index_path)
                self.index = faiss.IndexFlatIP(self.dimension)
                faiss.write_index(self.index, index_path)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

        self.index_path = index_path
        logger.info(type(self.index))

    def save(self):
        faiss.write_index(self.index, self.index_path)

    def add_embedding(self, embedding):

        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(vector)
        logger.info("Before Add: %s", self.index.ntotal)
        self.index.add(vector)
        logger.info("After Add: %s", self.index.ntotal)
        self.save()
        logger.info("After Save: %s", self.index.ntotal)
        logger.info("Index Path: %s", os.path.abspath(self.index_path))
        return self.index.ntotal - 1

    def search(self, embedding):

        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(vector)

        logger.info("Index Total: %s", self.index.ntotal)

        distances, indices = self.index.search(vector, 1)
        logger.info("Distances: %s", distances)
        logger.info("Indices: %s", indices)
        return {
            "score": float(distances[0][0]),
            "index": int(indices[0][0])
        }

    def rebuild_index(self, vectors) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        logger.info("Rebuilding FAISS index.")
        for embedding in vectors:
            vector = np.array(
                [embedding],
                dtype=np.float32
            )
            faiss.normalize_L2(vector)
            self.index.add(vector)

        self.save()
        logger.info("FAISS Index Rebuilt successfully. Total vector: %s", self.index.ntotal)