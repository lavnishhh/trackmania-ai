import cv2
import numpy as np

class rec:
    h = 480
    w = 640

recorder = rec()

frame = cv2.imread(r"""./ss1.png""")

while True:

    bw = frame

    bw = cv2.cvtColor(bw, cv2.COLOR_BGR2HSV)

    cv2.imshow('r', bw)

    
    lower = np.uint8([100, 9, 40])
    upper = np.uint8([200, 90, 100])
    bw = cv2.inRange(frame, lower, upper)

    bw = cv2.GaussianBlur(bw, (3,3), cv2.BORDER_DEFAULT)

    bw = cv2.inRange(frame, np.uint8([200]), np.uint8([255]))

    bw = cv2.resize(bw, (int(recorder.w/4), int(recorder.h/4)))

    # bw[60 : 120, 80 - 15: 80 + 15] = 0

    cv2.imshow('frame', bw)


    bw[int(recorder.h/8) - 15: int(recorder.h/4), int(recorder.w/8) - 15: int(recorder.w/8) + 15] = 0
    bw[int(recorder.h/8) + 10: int(recorder.h/4), int(recorder.w/8) - 25: int(recorder.w/8) + 25] = 0

    # cv2.imshow('frame', bw)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()