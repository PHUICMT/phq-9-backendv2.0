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

from ServerTask import *

app = Flask(__name__)
app.secret_key = 'PHQ@9@PHU@P@NON'
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=False , ping_timeout=600, ping_interval=600, async_handlers=True)
Payload.max_decode_packets = 500

# Not use for now
# models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
# backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

emotion_result = {
   "1": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "2": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "3": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "4": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "5": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "6": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "7": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "8": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
   "9": {"fear": 0, "happy": 0, "sad": 0, "neutral": 0},
}

print("[INFO] Server is started...")

directory_operation = DirectoryTask()
file_operation = FileTask()
general_operation = GeneralTask()

@socketio.on('user_connected')
def client_connect(user_data):
    print("[INFO] Client connected...")    
    saved_image_path = general_operation.get_image_path(user_data)
    saved_video_path = general_operation.get_video_path(user_data)
    
    print("[INFO] Image file path: ", saved_image_path)
    print("[INFO] Video file path: ", saved_video_path)

    directory_operation.create_image_directory(saved_image_path)
    directory_operation.create_video_directory(saved_video_path)

@socketio.on('end_section')
def end_section(user_data):
    print("[INFO] Client ending section...")
    saved_image_path = general_operation.get_image_path(user_data)
    saved_video_path = general_operation.get_video_path(user_data)
    video_path = saved_video_path + "/" + user_data['user_email'] + user_data['user_id'] + ".mp4"

    save_result = file_operation.save_video(saved_image_path, video_path)
    if save_result:
        print("[INFO] Video is saved...")
        emit('emotion', emotion_result)
        emit('start_disconect', True) #TODO send report to client
        
    
@socketio.on('disconnect')
def disconnect():
    print("[INFO] Client disconnected...")
    

@socketio.on('image')
def image(data_image): # Base64 encoded image
    print("[INFO] Image received...")
    time_stamp = data_image['timeStamp']
    image_base64 = data_image['imageBase64']
    article = data_image['article']
    image_file_path = general_operation.get_image_path(data_image) + "/" + str(time_stamp) + ".jpg"
    
    print("[INFO] [On Image] Image file path: ", image_file_path)
    
    # Decode image
    try:
        image_base64_decoded = base64.b64decode(image_base64)
        image_bytes = io.BytesIO(image_base64_decoded)
        image_file = Image.open(image_bytes)
        image_array = np.array(image_file)
        
        file_operation.save_image(image_file_path, image_base64_decoded)
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
    articleStr = str(article)
    resultStr = result_obj["dominant_emotion"]
    try:
        current_emotion = emotion_result[articleStr][resultStr]
        emotion_result[articleStr][resultStr] = current_emotion + 1
    except:
        print("[INFO] Emotion not found...")
    # print(emotion_result)
    # emit('emotion', emotion_result)
    
    
@app.route("/send-result", methods=['POST'])
def get_resutl():
    print("[INFO] Result received...")
    result = request.get_json()
    print(result)
    return "OK"
    

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=9000)
