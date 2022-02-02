import random
import time
from datetime import datetime
from difflib import SequenceMatcher

import cv2
import easyocr
from private import secrets
import imutils
import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt


def sms(number: list, link: str):
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = f"sender_id=FSTSMS&message={link}&language=english&route=q&numbers={','.join(number)}"

    headers = {
        "authorization": secrets.KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# video = cv2.VideoCapture('Data/test (1).mp4')

# key = illuminati.KEY

# database = pd.read_csv('data.csv')
# results = pd.read_csv('results.csv')
# history = ''
# nullCheck = 0

# plates = pd.DataFrame(columns=['Time', 'Plates'])

# # sms(['9006818029', '7772966141', '9123415629'], 'testing multiple numbers')

# k = 0
# while k != 2:
#     if nullCheck >= 50:
#         break

#     ret, img = video.read()

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

#     bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
#     edged = cv2.Canny(bfilter, 30, 200)

#     keypoints = cv2.findContours(
#         edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(keypoints)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

#     location = None
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 10, True)
#         if len(approx) == 4:
#             location = approx
#             break

#     mask = np.zeros(gray.shape, np.uint8)
#     new_image = cv2.drawContours(mask, [location], 0, 255, -1)
#     new_image = cv2.bitwise_and(img, img, mask=mask)
#     new = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

#     (x, y) = np.where(mask == 255)
#     (x1, y1) = (np.min(x), np.min(y))
#     (x2, y2) = (np.max(x), np.max(y))
#     cropped_image = gray[x1:x2+1, y1:y2+1]

#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(cropped_image)

#     try:
#         plate = result[0][1]

#         # TODO : Add similarity check for better accuracy

#         if plate in plate in database.Plate.to_string():
#             conInfo = database.iloc[np.where(
#                 database['Plate'] == plate)].Contact.to_string(index=False)

#         if history != plate:
#             sms([conInfo], 'testing concurrency')  # TODO :: Change in prod

#         nullCheck = 0
#         history = result[0][1]

#     except Exception as e:
#         print("Not Found !!!")
#         nullCheck += 1
#         print(e)

#     time.sleep(3)  # TODO :: Change in production
#     k += 1
