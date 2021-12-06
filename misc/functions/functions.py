import cv2
import numpy as np
import platform
from decouple import config
import time
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.camera import set_camera


# Takes action and defines the camera based on the OS type.
def os_action():
    if platform.system() == "Linux":
        while True:
            subprocess.run(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        set_camera.set_exposure()
        time.sleep(0.5)
        camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))

    if platform.system() != "Linux":
        while True:
            subprocess.call(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))
        time.sleep(1)
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        camera.set(15, int(config("WINDOWS_EXPOSURE")))
    return camera


# Takes a frame and returns the frame white balanced.
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


# Gets the dimensions of the camera.
def get_dimensions(camera, x_y):
    if x_y == "x":
        try:
            dim_x = camera.get(3)
        except Exception:
            dim_x = 0
        return dim_x
    if x_y == "y":
        try:
            dim_y = camera.get(4)
        except Exception:
            dim_y = 0
        return dim_y


# Calculates the distance between the crosshair and the hoop's center.
def calculate_rotation(x_defined, x, w):
    try:
        x_c = x + (x / 2)
        if x_c > (x_defined / 2):
            x_c = (x_c / 6) * 4.8
        return x_c - (x_defined / 2)
    except Exception:
        return None


# Calculates the focal length.
def calibrate(kpw, kd, kw):
    return (kpw * kd) / kw


# Calculates the distance between camera and the hoop.
def current_distance(kpw, kd, kw, w):
    try:
        return (kw * calibrate(kpw, kd, kw)) / w
    except Exception:
        pass


# Calculates the value of specified resolution divided by original camera resolution.
def resolution_rate(camera):
    return (int(config("FRAME_WIDTH")) / get_dimensions(camera, "x")), (
        int(config("FRAME_HEIGHT")) / get_dimensions(camera, "y")
    )


# Takes a frame and returns the frame with the crosshair drawn on it.
def crosshair(frame, camera=0):
    color = (0, 255, 0)
    x_rate, y_rate = (1, 1) if camera == 0 else resolution_rate(camera)
    fpt1 = (
        (int((((int(config("FRAME_WIDTH"))) / x_rate) / 2) - 20)),
        (int((int(config("FRAME_HEIGHT")) / y_rate) / 2)),
    )
    fpt2 = (
        (int((((int(config("FRAME_WIDTH"))) / x_rate) / 2) + 20)),
        (int((int(config("FRAME_HEIGHT")) / y_rate) / 2)),
    )
    spt1 = (
        (int((int(config("FRAME_WIDTH")) / x_rate) / 2)),
        (int((((int(config("FRAME_HEIGHT"))) / y_rate) / 2) - 20)),
    )
    spt2 = (
        (int((int(config("FRAME_WIDTH")) / x_rate) / 2)),
        (int((((int(config("FRAME_HEIGHT"))) / y_rate) / 2) + 20)),
    )

    crosshair = cv2.line(
        frame,
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


# Checks if the value is none.
def is_none(key):
    try:
        key = key + 1
        return 0
    except Exception:
        return 1


# Checks if the hoop is in the frame.
def is_detected(key):
    if is_none(key) == 0:
        return 1
    else:
        return 0


# Processes the frame, detects the cascade classifier and returns the frame with squares drawn on the detected object.
def vision(frame, cascade_classifier):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hoops = cascade_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if len(hoops) == 0:
        x, y, w, h = "none", "none", "none", "none"

    return frame, x, y, w, h


# Masks colors.
def mask_color(frame, lower, upper):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([lower])
    upper_range = np.array([upper])

    mask = cv2.inRange(hsv_frame, lower_range, upper_range)

    imask = mask > 0
    color = np.zeros_like(frame, np.uint8)
    color[imask] = frame[imask]

    return color


# Run Flask
def run_flask():
    if int(config("STREAM_FRAME")) == 1:
        return subprocess.Popen(["python", "misc/flask/flask_server.py"], shell=False)
