from threading import Timer
import os
import cv2
from darkflow.net.build import TFNet
import sys
from server.face_recognition.face_recognition.api import load_image_file, face_locations, face_encodings, compare_faces
import PIL.Image
import numpy as np
from keras.models import load_model
import time

def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x


current_path = os.getcwd() + "/server/helpers"

options = {"pbLoad": current_path + "/zhun-tiny-yolo-voc2.pb",
           "metaLoad": current_path + "/zhun-tiny-yolo-voc2.meta", "threshold": 0.1}

# emotionFile = 'fer2013_mini_XCEPTION.119-0.65.hdf5'
# emotionModel = load_model(emotionFile,compile=False)
# emotion_target_size = emotionModel.input_shape[1:3]
# emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


verified = ''

tfnet = TFNet(options)
## Load a sample picture and learn how to recognize it.
zhun_image = load_image_file(current_path + "/Zhun.jpg")
zhun_face_encoding = face_encodings(zhun_image)[0]

darius_image = load_image_file(current_path + "/Darius.jpg")
darius_face_encoding = face_encodings(darius_image)[0]

minh_image = load_image_file(current_path + "/Minh.jpg")
minh_face_encoding = face_encodings(minh_image)[0]

andri_image = load_image_file(current_path + "/Andri.jpg")
andri_face_encoding = face_encodings(andri_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    zhun_face_encoding,
    darius_face_encoding,
    minh_face_encoding,
    andri_face_encoding
]
known_face_names = [
    "Zhun",
    "Darius",
    "Minh",
    "Andri"
]


def update_data(interval):
    video_camera = cv2.VideoCapture(0)
    time.sleep(2)
    try:
        Timer(interval, update_data, [interval]).start()
        ret, frame = video_camera.read()
        faces = tfnet.return_predict(frame)

        if faces is not None:
            for face in faces:
                confidence = face.get('confidence')
                color = (0, 255, 0)
                if confidence <= 0.3:
                    pass
                else:
                    topLeft = face.get('topleft')
                    btmRight = face.get('bottomright')
                    tL = (topLeft.get('x'), topLeft.get('y'))
                    bR = (btmRight.get('x'), btmRight.get('y'))
                    _lw = 3
                    one = tL[0]
                    two = tL[1]
                    three = bR[0]
                    four = bR[1]
                    if (two < 0):
                        two = 0
                    if (four < 0):
                        four = 0
                    if (one < 0):
                        one = 0
                    if (three < 0):
                        three = 0
                    imCrop = frame[two:four, one:three]
                    # gray_face = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
                    # gray_face = cv2.resize(gray_face, (emotion_target_size))
                    rgb_imCrop = imCrop[:, :, ::-1]
                    # #Emotion detector
                    # gray_face = preprocess_input(gray_face, True)
                    # gray_face = np.expand_dims(gray_face, 0)
                    # gray_face = np.expand_dims(gray_face, -1)
                    # emotion_prediction = emotionModel.predict(gray_face)
                    # emotion_probability = np.max(emotion_prediction)
                    # emotion_label_arg = np.argmax(emotion_prediction)
                    # emotion_text = emotion_labels[emotion_label_arg]
                    face_encodes = face_encodings(rgb_imCrop)
                    global verified
                    if len(face_encodes) > 0:
                        face_encode = face_encodes[0]
                        # See if the face is a match for the known face(s)
                        matches = compare_faces(known_face_encodings, face_encode, tolerance=0.4)
                        name = "Unknown"
                        verified = False
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                            verified = True
                            video_camera.release()
                            cv2.destroyAllWindows()
                        return verified, name
    except Exception:
        video_camera.release()
        cv2.destroyAllWindows()
        return False, "Unknown"
