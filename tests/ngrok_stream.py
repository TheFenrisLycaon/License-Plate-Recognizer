import cv2
import numpy as np
import pandas as pd
from flask import Flask, Response, render_template

app = Flask(__name__)


def gen_frames():
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


global video, frame
video = cv2.VideoCapture("http://182.65.247.87:8082/stream170")

if video.isOpened() == False:
    print("Error opening video file")

running = False

plates = pd.DataFrame(columns=["Time", "Plates"])

print("Reading camera feed !")
while True:
    ret, img = video.read()
    frame = img
    h, w, c = img.shape
    img = img[: 10 * h // 15, w // 3 : 2 * w // 3]

    if not running:
        app.run(debug=False, host="127.0.0.1", port=5000)
        running = True


video.release()
cv2.destroyAllWindows()
__RESULTS__.to_csv("Out/results.csv")
