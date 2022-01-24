import cv2 as cv
import OCR
import os

#folder = "/home/user/Downloads/RoyalEnfield-20220122T102210Z-001/RoyalEnfield/"
plates_xml = "models/T34-208214-FP32.xml"
plates_bin = "models/T34-208214-FP32.bin"
ocr_model_xml = "models/Default.xml"
ocr_model_bin = "models/Default.bin"
detection_threshold = 0.3
#results_dir = "/home/user/Downloads/RoyalEnfield-20220122T102210Z-001/RoyalEnfieldOCR/"
img = "sample_images/000000944_0_TN18AJ7009.jpg"

# Load the model
net = cv.dnn.readNet( plates_xml, plates_bin )
# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# for img in os.listdir(folder):

frame = cv.imread(img)#'/home/user/Guardian_OpenVINO_V.1/misc/D43_20210308102029_000022568.jpg')
     
# Prepare input blob and perform inference
blob = cv.dnn.blobFromImage(frame, size=(304, 192), ddepth=cv.CV_8U)
net.setInput(blob)
out = net.forward()

platenumber = 0                   
# Draw detected bounding boxes on the frame
for detection in out.reshape(-1, 7):
    #print(detection[1])
    confidence = float(detection[2])
    xmin = int(detection[3] * frame.shape[1])
    ymin = int(detection[4] * frame.shape[0])
    xmax = int(detection[5] * frame.shape[1])
    ymax = int(detection[6] * frame.shape[0])

    if confidence > 0.3:
        plate = frame[ymin:ymax,xmin:xmax]
        number = OCR.license_plate_ocr(plate, ocr_model_xml, ocr_model_bin, detection_threshold )
        print(img,number)

        #cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
        #print(detection[1])

        # Save the frame to an image file
        #cv.imwrite(results_dir+img.split('_')[0]+"_"+str(platenumber)+"_"+str(number)+'.jpg', frame)#[ymin:ymax,xmin:xmax]) 
        #platenumber = platenumber + 1

    # else:
    #    cv.imwrite(results_dir+img.split('_')[0]+"_"+str(platenumber)+"_None"+'.jpg', frame)#[ymin:ymax,xmin:xmax]) 
