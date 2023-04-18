from keras.models import load_model
import cv2
import time
import win32gui
import win32ui
import win32con
import numpy as np
import math
import pandas as pd
import keyboard


df = pd.read_csv("data_cleaned.csv")
prediction_classes = list(df["input"].unique())

print(prediction_classes)

model = load_model('model.h5')

window_title = "Trackmania"
fps = 30

class WindowCapture:
    w = 640
    h = 480
    hwnd = None
    crop_x = 0
    crop_y = 0

    def __init__(self, window_title):
        self.hwnd = win32gui.FindWindow(None, window_title)
        # window_rect = win32gui.GetWindowRect(self.hwnd)

        border = 8
        titlebar = 30

        self.w = self.w - border*2
        self.h = self.h - (titlebar + border)
        
        self.crop_x = border
        self.crop_y = titlebar

    def capture(self):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.crop_x, self.crop_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img

recorder = WindowCapture(window_title)

curr_time = time.time()

i = 0
j = 0

prev_input = ''

angles = [-30, -40, -55, -65, -75, -90, -105, -115, -125, -140, -150]

while True:

    start_time = time.time()
    
    frame = recorder.capture()[150:, ]

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HLS)

    cv2.imshow('colored', frame)
    
    lower = np.uint8([100, 9, 20])
    upper = np.uint8([200, 100, 100])
    bw = cv2.inRange(frame, lower, upper)

    cv2.imshow('range', bw)


    bw = cv2.GaussianBlur(bw, (3,3), cv2.BORDER_DEFAULT)

    bw = cv2.resize(bw, (int(recorder.w/4), int(recorder.h/4)))

    bw = cv2.Canny(bw, 130, 140)

    bw[int(recorder.h/8) - 15: int(recorder.h/4), int(recorder.w/8) - 15: int(recorder.w/8) + 15] = 0
    bw[int(recorder.h/8) + 10: int(recorder.h/4), int(recorder.w/8) - 25: int(recorder.w/8) + 25] = 0

    h, w = bw.shape
    center_h = int(recorder.h/4 - 20)
    center_w = int(recorder.w/8)

    distances = []
    for angle in angles:
        y = center_h
        x = center_w

        while (x >= 0 and x < w) and (y >= 0 and y < h):

            image_x = int(x)
            image_y = int(y)
            if bw[image_y, image_x] == 255:
                bw[image_y - 2: image_y + 2, image_x - 2: image_x + 2] = 255
                break
            
            x += np.cos(math.radians(angle))
            y += np.sin(math.radians(angle))

        cv2.line(bw, (center_w, center_h), (image_x, image_y), 50)
        distances.append(math.dist([center_h, center_w], [image_y, image_x]))
    
    bw = cv2.resize(bw, (640,  480), cv2.INTER_CUBIC)
    cv2.imshow('frame', bw)
    pressed = ''

    test = np.array(distances)

    res = model.predict([distances])[0]
    key = prediction_classes[res.tolist().index(max(res))]
    print(key)
    key = prediction_classes[np.argmax(res)]

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    keyboard.press('w')
    
    for k in list(key):
        keyboard.press(k)
    
    time.sleep(0.06)

    keyboard.release('w')
    for k in list(key):
        keyboard.release(k)
    
    
    prev_input = pressed

    if((time.time() - start_time) < 1/fps):
        time.sleep(1/fps - (time.time() - start_time))