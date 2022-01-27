import cv2 as cv
import OCR


# Read an image
frame = cv.imread("/home/user/Guardian_OpenVINO_V.1/misc/000000010_3_TN09B6347.jpg")
ocr_model_xml = "/home/user/Guardian_OpenVINO_V.1/ir_weights/Default.xml"
ocr_model_bin = "/home/user/Guardian_OpenVINO_V.1/ir_weights/Default.bin"
detection_threshold = 0.4

# Call OCR Inference
print(OCR.license_plate_ocr(frame, ocr_model_xml, ocr_model_bin, detection_threshold))
