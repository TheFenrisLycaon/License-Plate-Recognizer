import cv2 as cv
from operator import itemgetter


def hardcoding(plate):
    int_to_char = {
        0: "Q",
        1: "T",
        2: "Z",
        3: "B",
        4: "A",
        5: "S",
        6: "G",
        7: "T",
        8: "B",
        9: "D",
    }
    char_to_int = {
        "A": 4,
        "B": 8,
        "C": 6,
        "D": 0,
        "E": 5,
        "F": 5,
        "G": 6,
        "H": 5,
        "I": 1,
        "J": 3,
        "K": 5,
        "L": 1,
        "M": 5,
        "N": 1,
        "O": 0,
        "P": 9,
        "Q": 0,
        "R": 5,
        "S": 9,
        "T": 7,
        "U": 0,
        "V": 1,
        "W": 4,
        "X": 4,
        "Y": 1,
        "Z": 2,
    }
    char_places = []
    if len(plate) == 10:
        char_places = [0, 1, 4, 5]
    elif len(plate) == 9:
        char_places = [0, 1, 4]
    else:
        char_places = [0, 1]
    new = ""
    for i in range(len(plate)):
        if i in char_places:
            if plate[i].isdigit():
                new += int_to_char[int(plate[i])]
            else:
                new += plate[i]
        else:
            if plate[i].isdigit():
                new += plate[i]
            else:
                new += str(char_to_int[(plate[i])])
    return new


# Dictionary to map predicted labels with characters
label_to_char_combined = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z",
    26: "0",
    27: "1",
    28: "2",
    29: "3",
    30: "4",
    31: "5",
    32: "6",
    33: "7",
    34: "8",
    35: "9",
}


def license_plate_ocr(image, model_xml, model_bin, char_threshold):

    # Load the model
    net = cv.dnn.readNet(model_xml, model_bin)
    # Specify target device
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    # Read an image
    frame = image  # cv.imread('000000010_3_TN09B6347.jpg')

    # Prepare input blob and perform an inference
    blob = cv.dnn.blobFromImage(frame, size=(304, 192), ddepth=cv.CV_8U)
    net.setInput(blob)
    out = net.forward()

    # Initialize values for Double-Line reordering
    C = []
    leftend = (0, 0)  # Top left
    rightend = (frame.shape[1], 0)  # Top right

    # Parse through detections
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        if confidence > char_threshold:
            xmin = int(detection[3] * frame.shape[1])
            ymin = int(detection[4] * frame.shape[0])
            xmax = int(detection[5] * frame.shape[1])
            ymax = int(detection[6] * frame.shape[0])

            xi = int(
                (xmin + xmax) / 2
            )  # Center of the bounding box of the detected character
            yi = int(
                (ymin + ymax) / 2
            )  # Center of the bounding box of the detected character

            C.append(
                (
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                    label_to_char_combined[int(detection[1])],
                    xi,
                    yi,
                )
            )  # List of characters and the corresponding attributes

    # Double-Line Checking Logic - NEEDS TO BE VALIDATED
    if len(C):  # If atleast 1 character is detected

        # print(sorted(C, key=itemgetter(6)))
        first = sorted(C, key=itemgetter(6))[0][6]
        sline = []
        dline = []
        sline.append(sorted(C, key=itemgetter(6))[0])
        for ch in sorted(C, key=itemgetter(6))[1:]:
            # print(ch)
            second = ch[6]
            if second - first > 14:
                dline.append(ch)
            else:
                sline.append(ch)

        l1 = "".join(
            map(str, list(map(itemgetter(4), sorted(sline, key=itemgetter(5)))))
        )
        # print("Line1",l1)
        l2 = "".join(
            map(str, list(map(itemgetter(4), sorted(dline, key=itemgetter(5)))))
        )
        # print("Line2",l2)
        plate = l1 + l2
        plate = list(plate)

        if len(plate) > 2:  # If plate has more than 2 characters
            if (
                plate[0] == "T" and plate[1] != "S"
            ):  # If first character is T and second character not S
                if plate[1] == "5":  # If second character is 5 then turn it into S
                    plate[1] = "S"
                else:  # Else turn second character into N
                    plate[1] = "N"

            plate = "".join(plate)
            plate = list(plate)

            if plate[0] == "N":  # If first character is N
                if plate[1] != "L":  # If second character is not L
                    if len(plate) != 10:  # If length of plate is not 10
                        plate.insert(0, "T")  # Insert T as the first character
            plate = "".join(plate)

        # if( len(plate)== 8 or len(plate)== 9 or len(plate)== 10 or len(plate)== 11 or len(plate)== 12 or len(plate)== 7 or len(plate)== 6 or len(plate)== 5 ): # If length of plate > 7 and < 11
        return hardcoding(plate)

    # # Draw detected faces on the frame
    # for detection in out.reshape(-1, 7):
    #     #print(detection[1])
    #     confidence = float(detection[2])
    #     xmin = int(detection[3] * frame.shape[1])
    #     ymin = int(detection[4] * frame.shape[0])
    #     xmax = int(detection[5] * frame.shape[1])
    #     ymax = int(detection[6] * frame.shape[0])

    #     if confidence > 0.3:
    #         cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
    #         print(detection[1],label_to_char_combined[int(detection[1])])

    # # Save the frame to an image file
    # cv.imwrite('out.png', frame)
