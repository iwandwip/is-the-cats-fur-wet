import serial
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster as Yolo

if __name__ == "__main__":
    cam = Vision(isUsingCam=False, addr="core/wet-cat.mp4") # open camera and load class, models
    pr = Yolo()
    pr.load("assets/class/cats.txt", "assets/data/cats.pt")
    try:
        while True:
            frame = cam.read(480, True)
            detect = pr.predict(frame)
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except RuntimeError:
        pass
