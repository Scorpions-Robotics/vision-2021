import cv2

cap = cv2.VideoCapture(0)
cap.set(15, -9)
ret, frame = cap.read()

while True:
    cv2.imshow("video", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 89:  # press 'y' to shoot
        cv2.imwrite("images/ref-pic.jpeg", frame)
        break

cv2.destroyAllWindows()
cap.release()
