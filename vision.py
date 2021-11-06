from networktables import NetworkTables
import numpy as np
import cv2
import os
import imutils
import zmq
import socket
import platform
from decouple import config
from set_camera import set_camera
import time


x = 0
y = 0
w = 0
h = 0
d = 0
r = 0

count = 0

KNOWN_WIDTH = int(config("KNOWN_WIDTH"))
KNOWN_PIXEL_WIDTH = int(config("KNOWN_PIXEL_WIDTH"))
KNOWN_DISTANCE = int(config("KNOWN_DISTANCE"))


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("vision")

if platform.system() == "Linux":
    while True:
        os.system("python fix_camera.py")
        break
    set_camera()
    time.sleep(0.5)
    camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))

if platform.system() != "Linux":
    while True:
        os.system("python fix_camera.py")
        break
    camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))
    time.sleep(1)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera.set(15, int(config("WINDOWS_EXPOSURE")))


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


def calculate_rotation():
    try:
        x_c = x + (x / 2) - (w / 4)
        location = x_c - (get_dimensions_x() / 2)
        rotate = location * -1
        return rotate
    except Exception:
        return None


def calibrate():
    FOCAL_LENGTH = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH
    return FOCAL_LENGTH


def current_distance():
    try:
        d = (KNOWN_WIDTH * calibrate()) / w
        return d
    except Exception:
        pass


def crosshair(x):
    color = (0, 255, 0)
    fpt1 = (
        (int(int(config("FRAME_WIDTH")) / 2) - 20),
        int(int(config("FRAME_HEIGHT")) / 2),
    )
    fpt2 = (
        (int(int(config("FRAME_WIDTH")) / 2) + 20),
        int(int(config("FRAME_HEIGHT")) / 2),
    )
    spt1 = (
        int(int(config("FRAME_WIDTH")) / 2),
        int((int(config("FRAME_HEIGHT")) / 2) - 20),
    )
    spt2 = (
        int(int(config("FRAME_WIDTH")) / 2),
        int((int(config("FRAME_HEIGHT")) / 2) + 20),
    )

    crosshair = cv2.line(
        x,
        fpt1,
        fpt2,
        color,
        2,
    )

    crosshair = cv2.line(
        crosshair,
        spt1,
        spt2,
        color,
        2,
    )
    return crosshair


def round_values():
    global x
    global y
    global w
    global h
    x = round(x)
    y = round(y)
    w = round(w)
    h = round(h)
    d = round(current_distance())
    r = round(calculate_rotation())
    return x, y, w, h, d, r


def is_detected(x):
    try:
        x = x + 1
        return 1
    except Exception:
        return 0


while True:

    grabbed, frame = camera.read()

    if grabbed == True:

        frame = imutils.resize(
            frame, width=int(config("FRAME_WIDTH")), height=int(config("FRAME_HEIGHT"))
        )

        if int(config("FLIP_FRAME")) == 1:
            frame = cv2.flip(frame, 1)

        frame = imutils.rotate(frame, int(config("FRAME_ANGLE")))

        if int(config("WHITE_BALANCE")) == 1:
            result = white_balance(frame)
            original = white_balance(frame)

        else:
            result = frame
            original = frame

        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        hoops = hoop_classifier.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
        )

        for (x, y, w, h) in hoops:
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = result[y : y + h, x : x + w]

        if len(hoops) == 0:
            x, y, w, h = "none", "none", "none", "none"

        try:
            x, y, w, h, d, r = round_values()

        except Exception:
            d = current_distance()
            r = calculate_rotation()

        b = is_detected(d)

        try:
            table.putNumber("X", x)
            table.putNumber("Y", y)
            table.putNumber("W", w)
            table.putNumber("H", h)
            table.putNumber("B", b)
            table.putNumber("D", d)
            table.putNumber("R", r)

        except Exception:
            table.putString("X", x)
            table.putString("Y", y)
            table.putString("W", w)
            table.putString("H", h)
            table.putNumber("B", b)
            table.putString("D", "none")
            table.putString("R", "none")

        if int(config("STREAM_FRAME")) == 1:
            encoded, buffer = cv2.imencode(".jpg", crosshair(original))
            footage_socket.send(buffer)

        if int(config("PRINT_VALUES")) == 1:
            print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b}")

        if int(config("SHOW_FRAME")) == 1:
            cv2.imshow("Original", crosshair(result))
            cv2.waitKey(1)

    else:
        if count == 0:
            print("No frame captured")
            count += 1
            break

camera.release()
cv2.destroyAllWindows()
