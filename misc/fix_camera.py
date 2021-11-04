import cv2
import time
from decouple import config
import platform
import set_camera

cap = cv2.VideoCapture(int(config("CAMERA_INDEX")))
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)

if platform.system() == "Linux":
    while True:
        set_camera.fix_camera_linux()
        ret, frame = cap.read()
        time.sleep(3)
        break

if platform.system() != "Linux":
    while True:
        ret, frame = cap.read()
        time.sleep(3)
        break

cap.release()
