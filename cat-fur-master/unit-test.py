from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster as Yolo

if __name__ == "__main__":
    cam = Vision(isUsingCam=True, addr="men.mp4")
    pr = Yolo()
    pr.load("assets/class/coco.txt", "assets/data/yolov5s.pt")
    try:
        while True:
            frame = cam.read(480, True)
            detect = pr.predict(frame)
            for i, data in enumerate(detect):
                print(data)
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except RuntimeError:
        pass
