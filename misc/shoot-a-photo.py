import cv2
import os
from set_camera import set_camera


set_camera()

os.chdir(os.path.dirname(__file__))

cap = cv2.VideoCapture(0)


while True:
    grabbed, frame = cap.read()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("y"):
        cv2.imwrite(f"../images/ref-pic.jpeg", frame)
        cv2.destroyAllWindows()
        break

cap.release()
