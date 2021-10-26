import cv2

cap = cv2.VideoCapture(1)
cap.set(15, -9)

while True:
    ret, frame = cap.read()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) & 0xFF == ord("y"):
        cv2.imwrite("../images/ref-pic.jpeg", frame)
        cv2.destroyAllWindows()
        break

cap.release()
