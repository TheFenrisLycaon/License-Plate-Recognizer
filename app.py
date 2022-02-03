from flask import Flask, Response, render_template

app = Flask(__name__)

# camera = cv2.VideoCapture(
#     'http://admin:v1ps*123@202.61.120.78:82/ISAPI/Streaming/channels/102/httpPreview')


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="192.168.244.43", port=8080)
