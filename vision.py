from networktables import NetworkTables
import numpy as np
import cv2
import imutils
import zmq


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("Vision")

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# camera.set(15, -9)

x = 0
y = 0
w = 0
h = 0

hoop_classifier = cv2.CascadeClassifier("cascade.xml")

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect("tcp://10.7.17.117:5555")

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

def calibrate():
    KNOWN_WIDTH = 39
    KNOWN_PIXEL_WIDTH = 
    KNOWN_DISTANCE = 
    FOCAL_LENGTH = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH

def current_distance():


while True:

    (
        grabbed,
        frame,
    ) = camera.read()

    try:

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

        table.putNumber("X", x)
        table.putNumber("Y", y)
        table.putNumber("W", w)
        table.putNumber("H", h)

        encoded, buffer = cv2.imencode(".jpg", result)
        footage_socket.send(buffer)

        # TODO: Remove below lines (until break (included)) lines before deploying to Jetson
        cv2.imshow("video", result)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:  # press 'ESC' to quit
            break

    except AttributeError as e:
        print(e)

camera.release()
cv2.destroyAllWindows()
