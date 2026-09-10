class FaceRecognitionException(Exception):
    pass

class NoFaceDetectionException(FaceRecognitionException):
    pass

class MultipleFaceRecognitionException(FaceRecognitionException):
    pass