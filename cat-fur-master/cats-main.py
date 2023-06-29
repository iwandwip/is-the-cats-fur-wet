from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster as Yolo
from utility.data import YAMLDataHandler

if __name__ == "__main__":
    print("[INFO] Main Initialize")
    cam = Vision(isUsingCam=False, addr="data/cats/wet-cat.mp4")
    yolo = Yolo()
    yolo.load("assets/class/cats.txt", "assets/data/cats.pt")
    data = YAMLDataHandler("out/cats-output-data.yaml")
    try:
        while True:
            frame = cam.read(480, True)
            detect = yolo.predict(frame)
            result = all(True if data['class'] == 'dry cat' else False for data in detect)
            data.update("condition", result)
            yolo.draw(frame, detect)
            cam.show(frame, "frame")
            cam.writeImg(frame, "out/cats-output.png")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except Exception as e:
        print(f"[INFO] Main Initialize Failed: \n{e}")
