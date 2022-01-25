import string
from datetime import datetime
from multiprocessing import Process
from typing import List

import cv2
import numpy as np
import pandas as pd
import requests
from flask import Flask, Response, render_template

from private import OCR, secrets

print("Reading Database")

__DATABASE__ = pd.read_csv('Out/data.csv')
__RESULTS__ = pd.read_csv('Out/results.csv')

app = Flask(__name__)


def gen_frames():
    while True:
        success, frame = video.read()
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


def sms(number: list, link: str):
    ''' Sends the link to client on the given number'''
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"sender_id=FSTSMS&message={link}&language=english&route=q&numbers={','.join(number)}"

    headers = {'authorization': secrets.KEY,
               'Content-Type': "application/x-www-form-urlencoded", 'Cache-Control': "no-cache", }

    response = requests.request("POST", url, data=payload, headers=headers)

    return (response.text)


def getInfo(plate: str) -> List:
    '''Returns the contact information as per the database'''
    # TODO :: Converted conInfo to a list for testing and demo. Change it to string and pass thru the SMS in a list in PROD
    if plate in plate in __DATABASE__.Plate.to_string():
        conInfo = __DATABASE__.iloc[np.where(
            __DATABASE__['Plate'] == plate)].Contact.to_string(index=False)
    else:
        print("Database entry doesn't exist")
        conInfo = []

    #! HARDCODED AS OF NOW CHANGE IN PRODUCTION
    conInfo = ['9445386095', '9123415629']
    return conInfo


def getLoc(out: np.ndarray) -> List[List]:
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * img.shape[1])
        ymin = int(detection[4] * img.shape[0])
        xmax = int(detection[5] * img.shape[1])
        ymax = int(detection[6] * img.shape[0])

        if confidence > 0.3:
            return True, [[xmin, xmax], [ymin, ymax]]

        return False, [[]]


def getOCR(plate: np.ndarray) -> List:
    # ocr_model_xml = "./Data/OCR.xml"
    # ocr_model_bin = "./Data/OCR.bin"
    # detection_threshold = 0.4
    # result = (OCR.license_plate_ocr(plate, ocr_model_xml,
    #       ocr_model_bin, detection_threshold))
    result = ['BR01AN3476']
    return result


net = cv2.dnn.readNet('./Data/plates-ssd.xml', './Data/plates-ssd.bin')
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
global video, frame
video = cv2.VideoCapture('Data/Deploy02.mp4')

if (video.isOpened() == False):
    print("Error opening video file")

server = Process(target=app.run)
firstFrame = None
history = ''
killDur = 0
running = False

plates = pd.DataFrame(columns=['Time', 'Plates'])

print("Reading camera feed !")
while True:
    ret, img = video.read()
    frame = img
    h, w, c = img.shape
    img = img[:10*h//15, w//3:2*w//3]
    motion = False

    if ret == True:
        cv2.imshow('Frame', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    blob = cv2.dnn.blobFromImage(img, size=(304, 192), ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()

    motion, location = getLoc(out)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    result = getOCR(img)

    if motion:
        cv2.rectangle(img, location[0], location[1], color=(0, 255, 0))
        cv2.imshow("Output", img)

        #! CHANGED. USING HARDCODED FOR TESTING
        # result = getOCR(img)
        try:
            plate = result[0]

            if len(plate) < 4:
                continue

            print("Plate found ::\t", plate, '\n')
            if history != plate:
                history = plate
                print("Sending...")
                # sms(getInfo(plate))
                app.run(debug=False, host='127.0.0.1', port=5000)
                running = True

        except Exception as e:
            print(e)
            if killDur >= 15:
                quit()
            elif running:
                if plate == '':
                    killDur += 1
            else:
                pass

    #     if firstFrame is None:
    #         firstFrame = gray
    #         continue

video.release()
cv2.destroyAllWindows()
__RESULTS__.to_csv('Out/results.csv')
