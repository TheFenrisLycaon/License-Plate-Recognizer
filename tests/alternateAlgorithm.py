import json
import os
from difflib import SequenceMatcher
from multiprocessing import Process

import cv2
import easyocr
import imutils
import numpy as np
import pandas as pd
import requests
from flask import Flask, Response, render_template
from private.secrets import KEY

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


def genLink(ip, port):
    print()
    os.system("curl  http://localhost:4040/api/tunnels > Data/tunnels.json")

    with open(r'Data\tunnels.json') as data_file:
        datajson = json.load(data_file)

    msg = []

    for i in datajson['tunnels']:
        msg.append(i['public_url'])

    return msg[1]


def sms(number: list):
    link = genLink('172.21.126.251', '5000')
    print('\n', link, '\n')
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"sender_id=FSTSMS&message={link}&language=english&route=q&numbers={','.join(number)}"

    headers = {'authorization': KEY,
               'Content-Type': "application/x-www-form-urlencoded", 'Cache-Control': "no-cache", }

    response = requests.request("POST", url, data=payload, headers=headers)
    # print(payload)
    print(response.text)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


global video, img

video = cv2.VideoCapture('Data/test01.mp4')

if (video.isOpened() == False):
    print("Error opening video file")

print("Reading Database")

__DATABASE__ = pd.read_csv('Out/data.csv')
__RESULTS__ = pd.read_csv('Out/results.csv')

server = Process(target=app.run)

history = ''
firstFrame = None
motion = False
killDur = 0
running = False

plates = pd.DataFrame(columns=['Time', 'Plates'])

print("Reading camera feed !")
while True:
    ret, img = video.read()
    frame = img
    h, w, c = img.shape
    img = img[h//5:4*h//5, w//3:2*w//3]

    # if ret == True:
    #     cv2.imshow('Frame', img)
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if firstFrame is None:
        firstFrame = gray
        continue

    delta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # NOTE : Uncomment to see input video
    if ret == True:
        cv2.imshow('Gray', gray)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # print("Waiting for motion...")
    for c in cnts:

        if cv2.contourArea(c) <= 100:
            motion = False
            continue
        else:
            # print(cv2.contourArea(c))
            motion = True

    if motion:
        print("Motion Triggered...\n")

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(bfilter, 30, 200)

        keypoints = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        mask = np.zeros(gray.shape, np.uint8)
        try:
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)

            new = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

            # NOTE : Uncomment to see the plate frame
            if ret == True:
                cv2.imshow('Frame', new_image)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            (x, y) = np.where(mask == 255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))

        except:
            pass

        cropped_image = gray[x1:x2+1, y1:y2+1]

        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        try:
            plate = result[0][1]

            print("Plate found ::\t", plate, '\n')

            # if plate in plate in __DATABASE__.Plate.to_string():
            #     conInfo = __DATABASE__.iloc[np.where(
            #         __DATABASE__['Plate'] == plate)].Contact.to_string(index=False)

            # TODO :: Converted conInfo to a list for testing and demo. Change it to string and pass thru the SMS in a list in PROD
            conInfo = ['9445386095', '9123415629']

            if not running:
                print("Sending...")
                sms(conInfo)
                app.run(debug=False, host='127.0.0.1', port=5000)
                running = True

            history = result[0][1]

        except Exception as e:
            if killDur >= 15:
                exit()
            elif running:
                killDur += 1
            else:
                pass

video.release()
cv2.destroyAllWindows()
__RESULTS__.to_csv('Out/results.csv')
