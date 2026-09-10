from insightface.app import FaceAnalysis
import cv2

class FaceService:
    def __init__(self):
        self.app = FaceAnalysis(
            providers=['CPUExceptionProvider']
        )
        self.app.prepare(ctx_id=0)

    def detect_faces(self, image_path: str):
        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Unable to load image")

        faces = self.app.get(image)

        return faces