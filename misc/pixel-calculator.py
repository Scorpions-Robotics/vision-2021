from networktables import NetworkTables
import numpy as np
import cv2
import imutils

x = 0
y = 0
w = 0
h = 0

hoop_classifier = cv2.CascadeClassifier("../cascade.xml")


def white_balance(frame):
    result = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - (
        (avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result[:, :, 2] = result[:, :, 2] - (
        (avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result


try:
    frame = cv2.imread("../images/ref-pic.jpeg")
    frame = imutils.rotate(frame, angle=0)

    result = white_balance(frame)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    hoops = hoop_classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = result[y : y + h, x : x + w]

    print(x, y, w, h)

    cv2.imwrite("../images/ref-pic-post.jpeg", result)

    cv2.imshow("result", result)
    k = cv2.waitKey(5000) & 0xFF

except AttributeError as e:
    print(e)

cv2.destroyAllWindows()
