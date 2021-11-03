import cv2
import os
import platform
from set_camera import set_camera

if platform.system() == "Linux":
    set_camera()

camera = cv2.VideoCapture(0)

if platform.system() != "Linux":
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera.set(15, -10)

os.chdir(os.path.dirname(__file__))

while True:
    grabbed, frame = camera.read()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("y"):
        cv2.imwrite(f"../images/ref-pic.jpeg", frame)
        cv2.destroyAllWindows()
        break

camera.release()
