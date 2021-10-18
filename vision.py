from networktables import NetworkTables
import numpy as np
import cv2
import imutils


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("Vision")

camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(15, -8)

x = 0
y = 0
w = 0
h = 0

hoop_classifier = cv2.CascadeClassifier("cascade.xml")

while True:

    (
        grabbed,
        frame,
    ) = camera.read()

    frame = imutils.rotate(frame, angle=0)

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

    result = white_balance(frame)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    faces = hoop_classifier.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = result[y : y + h, x : x + w]

    print(x, y, w, h)

    table.putNumber("X", x)
    table.putNumber("Y", y)
    table.putNumber("W", w)
    table.putNumber("H", h)

    cv2.imshow("video", result)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:  # press 'ESC' to quit
        break

camera.release()
cv2.destroyAllWindows()
