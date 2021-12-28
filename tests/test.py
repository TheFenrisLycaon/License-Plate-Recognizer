import cv2


video = cv2.VideoCapture('Data/Deploy02.mp4')

if (video.isOpened() == False):
    print("Error opening video  file")

while(video.isOpened()):
    ret, img = video.read()
    frame = img
    h, w, c = img.shape
    img = img[h//:10*h//15, w//3:2*w//3]

    if ret == True:
        cv2.imshow('Frame', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
