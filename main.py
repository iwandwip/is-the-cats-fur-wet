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
RECEIVER_TIME = 1000

def millis():
    return int(time.time() * 1000)

if __name__ == "__main__":
    cam = Vision(False, "core/cat.mp4")
    pr = ImgBuster()
    pr.load("assets/class/cats.txt", "assets/data/best.pt")
    coms = serial.Serial('COM6', 9600, timeout=1)
    coms.reset_input_buffer()
    taskTimer = [0, 0, 0]
    stateCatFur = CAT_FUR_WET
    try:
        while True:
            frame = cam.read(480, True)
            if (millis() - taskTimer[0] >= DETECT_TIME):
                detect = pr.predict(frame)
                for i, data in enumerate(detect):
                    if detect[i]['class'] == 'kucing_basah':
                        stateCatFur = CAT_FUR_WET
                    elif detect[i]['class'] == 'kucing_kering':
                        stateCatFur = CAT_FUR_DRY
                taskTimer[0] = millis()
            if (millis() - taskTimer[1] >= SEND_TIME):
                if stateCatFur:
                    coms.write(b"1\n")
                else:
                    coms.write(b"0\n")
                taskTimer[1] = millis()
            if (millis() - taskTimer[2] >= RECEIVER_TIME):
                if coms.in_waiting > 0:
                    data = coms.readline().decode('utf-8', 'ignore').strip().split()
                    data = [value.replace('C', '') for value in data]
                taskTimer[2] = millis()
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except RuntimeError:
        pass
