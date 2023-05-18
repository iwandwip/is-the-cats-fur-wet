from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster
import serial
import time
import random

# constant macros
CAT_FUR_WET = 0
CAT_FUR_DRY = 1

DETECT_TIME = 50
SEND_TIME = 1000

def millis():
    return int(time.time() * 1000)

if __name__ == "__main__":
    cam = Vision(False, "core/wet-cat.mp4")
    pr = ImgBuster()
    pr.load("assets/class/cats.txt", "assets/data/best.pt")
    # coms = serial.Serial('COM7', 9600)
    # coms.timeout = 1
    taskTimer = 0
    detectTimer = 0
    stateCatFur = CAT_FUR_WET
    try:
        while True:
            frame = cam.read(480, True)
            if (millis() - detectTimer >= DETECT_TIME):
                detect = pr.predict(frame)
                for i, data in enumerate(detect):
                    if detect[i]['class'] == 'kucing_basah':
                        stateCatFur = CAT_FUR_WET
                    elif detect[i]['class'] == 'kucing_kering':
                        stateCatFur = CAT_FUR_DRY
                detectTimer = millis()
            if (millis() - taskTimer >= SEND_TIME):
                print(random.randint(0, 200) * 0.1)
                taskTimer = millis()
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except RuntimeError:
        pass
