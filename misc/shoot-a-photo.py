import cv2
import os
import platform
import imutils
from decouple import config
import time
from ..functions import set_camera


count = 0

os.chdir(os.path.dirname(__file__))

if platform.system() == "Linux":
    while True:
        os.system("python fix_camera.py")
        break
    set_camera.set_camera()
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

while True:
    grabbed, frame = camera.read()

    if grabbed == True:

        frame = imutils.resize(
            frame, width=int(config("FRAME_WIDTH")), height=int(config("FRAME_HEIGHT"))
        )
        cv2.imshow("img", frame)
        if cv2.waitKey(1) & 0xFF == ord("y"):
            cv2.imwrite(f"../images/ref-pic.jpeg", frame)
            cv2.destroyAllWindows()
            break

    else:
        if count == 0:
            print("No frame captured")
            count += 1
            break

camera.release()
