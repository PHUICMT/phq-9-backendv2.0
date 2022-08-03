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
app.secret_key = 'PHQ@9@PHU@P@NON'
socketio = SocketIO(app, cors_allowed_origins="*")
Payload.max_decode_packets = 500
video_out = None

# Not use for now
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

print("[INFO] Server is started...")

video_path = "./video_storage/"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
imageWidth = 400
imageHeight = 300
fps = 6

@socketio.on('user_connected')
def client_connect(user_data):
    print("[INFO] Client connected...")
    user_email = user_data['user_email']
    user_id = user_data['user_id']
    file_name = user_email + "_" + user_id + ".avi"
    video_out = cv2.VideoWriter(video_path + file_name, fourcc, fps, (imageWidth, imageHeight))

@socketio.on('disconnect')
def disconnected():
    print("[INFO] Client disconnected...")
    # if video_out is not None:
    #     video_out.release()
    #     video_out = None

@socketio.on('image')
def image(data_image): # Base64 encoded image
    print("[INFO] Image received...")
    time_stamp = data_image['timeStamp']
    image_base64 = data_image['imageBase64']

    # Decode image
    try:
        image_base64_decoded = base64.b64decode(image_base64)
        image_bytes = io.BytesIO(image_base64_decoded)
        image_file = Image.open(image_bytes)
        image_array = np.array(image_file)

        if video_out is not None:
            video_out.write(cv2.imdecode(np.fromstring(image_base64_decoded, dtype=np.uint8), cv2.IMREAD_COLOR))
    except:
        print("[ERROR] Image decoding failed...")
        return

    # Detect faces emotion
    print("[INFO] Detecting faces...")
    try: 
        result_obj = DeepFace.analyze(img_path = image_array, actions = ['emotion'], enforce_detection=True)
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