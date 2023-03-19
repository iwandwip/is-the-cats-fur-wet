from modules.utils import *
from modules.process import Routine
from modules.image import Vision
from modules.filters import KalmanFilter1D

if __name__ == "__main__":
    cam = Vision(True)
    rt = Routine()
    rt.load("assets/data/data.weights",
            "assets/config/config.cfg",
            "assets/class/class.names")
    while True:
        frame = cam.read(frame_size=480, show_fps=True)
        detect = rt.get(frame)
        cam.show(frame, "frame")
        cam.wait(1)
