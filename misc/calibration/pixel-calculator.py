import cv2
import os


os.chdir(os.path.dirname(__file__))

x = 0
y = 0
w = 0
h = 0

hoop_classifier = cv2.CascadeClassifier("../../cascade.xml")


try:
    frame = cv2.imread("../../images/ref-pic.jpeg")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hoops = hoop_classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]

    if len(hoops) == 0:
        x, y, w, h = "none", "none", "none", "none"

    print(x, y, w, h)

    cv2.imwrite("../../images/ref-pic-post.jpeg", frame)

    cv2.imshow("result", frame)
    k = cv2.waitKey(5000) & 0xFF

except AttributeError as e:
    print(e)

cv2.destroyAllWindows()
