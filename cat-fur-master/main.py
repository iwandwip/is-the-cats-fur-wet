from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster as Yolo
from utility.data import YAMLDataHandler

if __name__ == "__main__":
    cam = Vision(isUsingCam=True)
    yolo = Yolo()
    yolo.load("assets/class/coco.txt", "assets/data/yolo5.pt")
    data = YAMLDataHandler("out/output.yaml")
    try:
        while True:
            frame = cam.read(1080, True)
            detect = yolo.predict(frame)
            yolo.draw(frame, detect)
            cam.show(frame, "frame")

            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except Exception as e:
        print(e)
