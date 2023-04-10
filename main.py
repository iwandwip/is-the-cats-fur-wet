from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgRex
# import rospy

if __name__ == "__main__":
    cam = Vision(False, "core/cats.mp4")
    pr = ImgRex()
    pr.load("datasets/cat.weights",
            "datasets/cat.cfg",
            "datasets/cat.txt")
    try:
        while True:
            frame = cam.read(480, True)
            detect = pr.predict(frame)
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            cam.wait(1)
    except RuntimeError:
        pass
