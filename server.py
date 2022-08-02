from flask import Flask, request
from flask_socketio import SocketIO, emit
from io import StringIO
from PIL import Image
import numpy as np
import io
import cv2, base64

app = Flask(__name__)
app.secret_key = '1111'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    # b = io.BytesIO(base64.b64decode(data_image))
    print("---------------------------------------------------------------")
    print(data_image)
    # pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # # Process the image frame
    # frame = imutils.resize(frame, width=700)
    # frame = cv2.flip(frame, 1)
    # imgencode = cv2.imencode('.jpeg', frame)[1]

    # # base64 encode
    # stringData = base64.b64encode(imgencode).decode('utf-8')
    # b64_src = 'data:image/jpeg;base64,'
    # stringData = b64_src + stringData

    # emit the frame back
    # emit('response_back', stringData)
    emit('response_back', data_image)
    

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=9000)