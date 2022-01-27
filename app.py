import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

# camera = cv2.VideoCapture(
#     'http://admin:v1ps*123@202.61.120.78:82/ISAPI/Streaming/channels/102/httpPreview')

camera = cv2.VideoCapture('Data/Deploy02.mp4')


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
