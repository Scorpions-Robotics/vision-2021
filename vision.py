from networktables import NetworkTables
import cv2
import imutils
import zmq
import socket
from decouple import config
from misc.functions import functions


x = 0
y = 0
w = 0
h = 0
d = 0
r = 0


kpw = int(config("KNOWN_PIXEL_WIDTH"))
kd = int(config("KNOWN_DISTANCE"))
kw = int(config("KNOWN_WIDTH"))


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("vision")


camera = functions.os_action()

cascade_classifier = cv2.CascadeClassifier("cascade.xml")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f"tcp://{local_ip}:5555")


while True:
    try:

        grabbed, original = camera.read()

        if grabbed == True:

            frame = original

            frame = imutils.resize(
                frame,
                width=int(config("FRAME_WIDTH")),
                height=int(config("FRAME_HEIGHT")),
            )

            if int(config("FLIP_FRAME")) == 1:
                frame = cv2.flip(frame, 1)

            frame = imutils.rotate(frame, int(config("FRAME_ANGLE")))

            if int(config("WHITE_BALANCE")) == 1:
                frame = functions.white_balance(frame)

            result, x, y, w, h = functions.vision(frame, cascade_classifier)

            d = functions.current_distance(kpw, kd, kw, w)
            r = functions.calculate_rotation(camera, x, w)
            b = functions.is_detected(d)

            if b == 0:
                table.putString("X", "none")
                table.putString("Y", "none")
                table.putString("W", "none")
                table.putString("H", "none")
                table.putString("D", "none")
                table.putString("R", "none")
                table.putString("B", "0")

                if int(config("PRINT_VALUES")) == 1:
                    print("X: none Y: none W: none H: none D: none R: none B: 0")

            elif b == 1:
                d = round(d)
                r = round(r)
                table.putNumber("X", x)
                table.putNumber("Y", y)
                table.putNumber("W", w)
                table.putNumber("H", h)
                table.putNumber("D", d)
                table.putNumber("R", r)
                table.putNumber("B", 1)

                if int(config("PRINT_VALUES")) == 1:
                    print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: 1")

            if int(config("STREAM_FRAME")) == 1:
                encoded, buffer = cv2.imencode(".jpg", functions.crosshair(original))
                footage_socket.send(buffer)

            if int(config("SHOW_FRAME")) == 1:
                cv2.imshow("Result", functions.crosshair(result))
                cv2.waitKey(1)

        else:
            try:
                camera = functions.os_action()
            except Exception:
                pass

    except KeyboardInterrupt:
        break

camera.release()
cv2.destroyAllWindows()
