import cv2
import os
import platform
from decouple import config
import time
from set_camera import set_camera

os.chdir(os.path.dirname(__file__))

if platform.system() == "Linux":
    while True:
        os.system("python fix_camera.py")
        break
    time.sleep(2)
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
    time.sleep(1)
    camera.set(15, int(config("WINDOWS_EXPOSURE")))

while True:
    grabbed, frame = camera.read()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("y"):
        cv2.imwrite(f"../images/ref-pic.jpeg", frame)
        cv2.destroyAllWindows()
        break

camera.release()
