from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster
# import rospy

if __name__ == "__main__":
    cam = Vision(False, "core/wet-cat.mp4")
    pr = ImgBuster()
    pr.load("assets/class/cats.txt", "assets/data/best.pt")
    try:
        while True:
            frame = cam.read(480, True)
            detect = pr.predict(frame)
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            cam.wait(1)
    except RuntimeError:
        pass
