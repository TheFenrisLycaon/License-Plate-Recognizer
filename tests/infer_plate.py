import cv2


# Load the model
net = cv2.dnn.readNet("./Data/plates-ssd.xml", "./Data/plates-ssd.bin")

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Read an image
frame = cv2.imread("Data/test.jpg")

# Prepare input blob and perform inference
blob = cv2.dnn.blobFromImage(frame, size=(304, 192), ddepth=cv2.CV_8U)
net.setInput(blob)
out = net.forward()


# Draw detected bounding boxes on the frame
for detection in out.reshape(-1, 7):
    # print(detection[1])
    confidence = float(detection[2])
    xmin = int(detection[3] * frame.shape[1])
    ymin = int(detection[4] * frame.shape[0])
    xmax = int(detection[5] * frame.shape[1])
    ymax = int(detection[6] * frame.shape[0])

    if confidence > 0.3:
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
        print(detection[1])

# Save the frame to an image file
cv2.imwrite("Out/out.png", frame)
