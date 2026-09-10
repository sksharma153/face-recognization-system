class FaceRecognitionException(Exception):
    """Base exception for all face recognition errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class FaceNotDetectedException(FaceRecognitionException):
    pass

class PersonNotFoundException(FaceRecognitionException):
    pass

class DuplicatePersonException(FaceRecognitionException):
    pass

class FaissSearchException(FaceRecognitionException):
    pass

class MultipleFacesDetectedExceptions(FaceRecognitionException):
    pass

class EmbeddingGenerationException(FaceRecognitionException):
    pass

class FaissException(FaceRecognitionException):
    pass

class DatabaseException(FaceRecognitionException):
    pass