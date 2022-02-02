from typing import List

import cv2

video = cv2.VideoCapture("Data/Deploy02.mp4")

# Load the model
net = cv2.dnn.readNet("Data/bike.xml", "Data/bike.bin")

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

while True:
    check, frame = video.read()

    # Prepare input blob and perform inference
    blob = cv2.dnn.blobFromImage(frame, size=(304, 192), ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()

    # Draw detected bounding boxes on the frame
    for detection in out.reshape(-1, 7):
        # print(str(detection[1]))
        confidence = float(detection[2])
        # print(confidence)
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])

        if (
            confidence > 0.9
            and str(detection[1]) == "2.0"
            or str(detection[1]) == "4.0"
        ):
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
            print(detection[1])

    if check == True:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            video.release()
            cv2.destroyAllWindows()
            break
