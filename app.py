import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

camera = cv2.VideoCapture("http://182.65.247.87:8080/stream169")


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            camera = cv2.VideoCapture("http://182.65.247.87:8080/stream169")
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")

,
@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
