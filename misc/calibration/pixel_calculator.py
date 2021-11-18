import cv2
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import functions


x = 0
y = 0
w = 0
h = 0

cascade_classifier = cv2.CascadeClassifier("cascade.xml")

while True:
    try:
        frame = cv2.imread("images/ref-pic.jpeg")

        result, x, y, w, h = functions.vision(frame, cascade_classifier)

        print(f"X: {x} Y: {y} W: {w} H: {h}")

        cv2.imshow("img", result)
        if cv2.waitKey(1) & 0xFF == ord("y"):
            cv2.imwrite(f"images/ref-pic-post.jpeg", result)
            print("Processed image is written under images folder.")
            break

    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
