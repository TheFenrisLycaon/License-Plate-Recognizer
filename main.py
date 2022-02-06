import subprocess
import time
import urllib.parse
import urllib.request
from typing import List

import cv2
import numpy as np
import pandas as pd
import requests

from private import secrets

print("Reading Database")

__DATABASE__ = pd.read_csv("Out/data.csv")
__RESULTS__ = pd.read_csv("Out/results.csv")

# subprocess.run("initial.bat", shell=True)


def sendSMS(numbers, sender, message):
    """Sends SMS using TEXTLOCAL"""
    #! Currently not working for unknown resaons.
    params = {
        "apikey": secrets.LOCAL,
        "numbers": numbers,
        "message": message,
        "sender": sender,
    }
    f = urllib.request.urlopen(
        "https://api.textlocal.in/send/?" + urllib.parse.urlencode(params)
    )
    return (f.read(), f.code)


def sms(number: list, link: str):
    """Sends the link to client on the given number"""
    # TODO : To be upgrded to a new API once finalized.
    url = "https://api.textlocal.in/send/"

    payload = f"sender_id=FSTSMS&message={link}&language=english&route=q&numbers={','.join(number)}"

    headers = {
        "authorization": secrets.KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def getInfo(plate: str) -> List:
    """Returns the contact information as per the database"""
    # TODO :: Converted conInfo to a list for testing and demo. Change it to string and pass thru the SMS in a list in PROD
    # if plate in plate in __DATABASE__.Plate.to_string():
    #     conInfo = __DATABASE__.iloc[
    #         np.where(__DATABASE__["Plate"] == plate)
    #     ].Contact.to_string(index=False)
    # else:
    #     print("Database entry doesn't exist")
    #     conInfo = []

    #! HARDCODED AS OF NOW CHANGE IN PRODUCTION
    conInfo = ["9445386095", "9123415629"]
    return conInfo


def getOCR(plate: np.ndarray) -> List:
    # ocr_model_xml = "./Data/OCR.xml"
    # ocr_model_bin = "./Data/OCR.bin"
    # detection_threshold = 0.4
    # result = OCR.license_plate_ocr(
    #     plate, ocr_model_xml, ocr_model_bin, detection_threshold
    # )
    result = ["BR01AN3476"]
    return result


def getLink():
    pass


net = cv2.dnn.readNet("./models/plate.xml", "./models/plate.bin")
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
global video, frame

#! CHANGE LIVE LINKS
video = cv2.VideoCapture("./Data/Deploy02.mp4")
time.sleep(1)
if video.isOpened() == False:
    print("Error opening video file")

firstFrame = None
history = ""
killDur = 0
running = False
result = []
plates = pd.DataFrame(columns=["Time", "Plates"])

ngrok = subprocess.Popen(["ngrok", "http", "-region", "in", "http://localhost:9090"])


print("Reading camera feed !")
while True:
    ret, img = video.read()
    frame = img
    h, w, c = img.shape
    img = img[: 10 * h // 15, w // 3 : 2 * w // 3]
    motion = False

    if ret == True:
        cv2.imshow("Frame", img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    blob = cv2.dnn.blobFromImage(frame, ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()
    location = []

    for detection in out.reshape(-1, 7):
        # print(detection[1])
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])

        if confidence > 0.3:
            location.append([[xmin, ymin], [ymin, ymax]])
            motion = True
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if motion:
        # cv2.imshow("Output", img)
        cropped_img = img[
            location[0][0][0] : location[0][0][1], location[0][1][0] : location[0][1][1]
        ]

        #! CHANGED. USING HARDCODED FOR TESTING
        if not result:
            result = getOCR(cropped_img)

        plate = ""
        try:
            plate = result[0]

            if len(plate) < 4:
                continue

            print("Plate found ::\t", plate, "\n")
            if history != plate:
                history = plate
                print("Sending...")
                # sms(getInfo(plate), getLink())
                # The following line is for UNIX systems on which we'll most linkely be deploying. Uncomment to test.
                # if not running:
                # app = subprocess.Popen("python2 ./utils/mjpg_serve_2.py", shell=True)

                # On conda defined environments, a different approach is followed.
                # Uncomment the following line in production or while testing...
                if not running:
                    app = subprocess.Popen(
                        "conda activate arima &&  python ./utils/mjpg_serve_2.py",
                        shell=True,
                    )
                running = True

        except Exception as e:
            print(e)
            if killDur >= 15:
                ngrok.terminate()
            elif running:
                if plate == "":
                    killDur += 1
            else:
                pass

video.release()
ngrok.kill()
ngrok.terminate()
cv2.destroyAllWindows()
__RESULTS__.to_csv("Out/results.csv")
