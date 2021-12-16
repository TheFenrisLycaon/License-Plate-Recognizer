import cv2


video = cv2.VideoCapture('Data/test00.mp4')

if (video.isOpened() == False):
    print("Error opening video  file")

while(video.isOpened()):
    ret, frame = video.read()
    
    if ret == True:
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
