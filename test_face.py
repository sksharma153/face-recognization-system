import cv2
from app.services.face_service import FaceService

service = FaceService()

faces = service.detect_faces("app/storage/images/Sandeep.jpg")

print("Face Found:", len(faces))
if len(faces) > 0:
    face = faces[0]
    print("Embedding Length:", len(face.embedding))
    print("Bounding Box:", face.bbox)
