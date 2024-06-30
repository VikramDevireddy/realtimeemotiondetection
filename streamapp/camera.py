from tensorflow.keras.models import load_model
from deepface import DeepFace
import cv2
import os
import numpy as np
from django.conf import settings

face_detection_videocam = cv2.CascadeClassifier(
    os.path.join(
        settings.BASE_DIR, "opencv_haarcascade_data/haarcascade_frontalface_default.xml"
    )
)
face_detection_webcam = cv2.CascadeClassifier(
    os.path.join(
        settings.BASE_DIR, "opencv_haarcascade_data/haarcascade_frontalface_default.xml"
    )
)
# load our serialized face detector model from disk
prototxtPath = os.path.sep.join([settings.BASE_DIR, "face_detector/deploy.prototxt"])
weightsPath = os.path.sep.join(
    [settings.BASE_DIR, "face_detector/res10_300x300_ssd_iter_140000.caffemodel"]
)
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model(
    os.path.join(settings.BASE_DIR, "face_detector/mask_detector.model")
)

rar = []


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.rar = []

    def __del__(self):
        self.video.release()

    def get_arr(self):
        return rar

    def get_frame(self):
        success, image = self.video.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )
        for x, y, w, h in faces_detected:
            cv2.rectangle(
                image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2
            )
        result = DeepFace.analyze(image, actions=["emotion"], enforce_detection=False)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SIMPLEX
        rar.append(result[0]["dominant_emotion"])
        cv2.putText(
            image,
            result[0]["dominant_emotion"],
            (50, 50),
            font,
            3,
            (0, 0, 255),
            2,
            cv2.LINE_4,
        )
        ret, jpeg = cv2.imencode(".jpg", image)
        jpeg = np.array(jpeg)
        return jpeg.tobytes()
