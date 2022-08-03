from flask import Flask, request
from flask_socketio import SocketIO, emit
from engineio.payload import Payload
from io import StringIO
from PIL import Image
from deepface import DeepFace
import numpy as np
import io
import cv2, base64
import json

app = Flask(__name__)
app.secret_key = '1111'
socketio = SocketIO(app, cors_allowed_origins="*")
Payload.max_decode_packets = 500

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

print("[INFO] Server is started...")

@socketio.on('image')
def image(data_image): #Base64 encoded image
    time_stamp = data_image['timeStamp']
    image_base64 = data_image['imageBase64']

    print("[INFO] Image received...")

    # Decode image
    try:
        image_base64_decoded = base64.b64decode(image_base64)
        image_bytes = io.BytesIO(image_base64_decoded)
        image_file = Image.open(image_bytes)
        image_array = np.array(image_file)
    except:
        print("[ERROR] Image decoding failed...")
        return

    # Detect faces emotion
    print("[INFO] Detecting faces...")
    try: 
        result_obj = DeepFace.analyze(img_path = image_array, actions = ['emotion'], enforce_detection=False)
    except:
        result_obj = {"dominant_emotion": "Unknown"}
        

    print("[INFO] Faces detected...")
    print("Emote : " + result_obj["dominant_emotion"] + " Time : " + str(time_stamp))

    try:
        emit('response_back', result_obj) #Response back
    except:
        print("[ERROR] Cannot send response back...")
        pass
    

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=9000)