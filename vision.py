from networktables import NetworkTables
import numpy as np
import cv2
import imutils
import zmq
import socket


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("Vision")

camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(15, -9)

x = 0
y = 0
w = 0
h = 0
d = 0
r = 0

hoop_classifier = cv2.CascadeClassifier("cascade.xml")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f"tcp://{local_ip}:5555")


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


KNOWN_WIDTH = 39
KNOWN_PIXEL_WIDTH = 172
KNOWN_DISTANCE = 171


def get_dimensions_x():
    try:
        dim_x = camera.get(3)
        return dim_x
    except Exception:
        dim_x = 0
        return dim_x


def get_dimensions_y():
    try:
        dim_y = camera.get(4)
        return dim_y
    except Exception:
        dim_y = 0
        return dim_y


def get_cc():
    for i in hoops:
        M = cv2.moments(i)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(result, (int(cx), int(cy)), (0, 255, 255), 2)
            return cx, cy


def calculate_rotation():
    r_x, r_y = get_cc()
    location = r_x - (get_dimensions_x() / 2)
    rotate = location * -1
    return rotate


def calibrate():
    FOCAL_LENGTH = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
    return FOCAL_LENGTH


def current_distance():
    d = (KNOWN_WIDTH * calibrate()) / w
    return d


while True:

    (
        grabbed,
        frame,
    ) = camera.read()

    try:

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

            d = current_distance()
            r = calculate_rotation()

            print(x, y, w, h, d, r)

            table.putNumber("X", x)
            table.putNumber("Y", y)
            table.putNumber("W", w)
            table.putNumber("H", h)
            table.putNumber("D", d)
            table.putNumber("R", r)

            encoded, buffer = cv2.imencode(".jpg", result)
            footage_socket.send(buffer)

            cv2.imshow("video", result)
            k = cv2.waitKey(30) & 0xFF
            if k == 27:  # press 'ESC' to quit
                break

        except KeyboardInterrupt:
            break

    except AttributeError as e:
        print(e)

camera.release()
cv2.destroyAllWindows()
