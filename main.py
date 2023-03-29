from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter1D
from modules.process import Routine, Procedure
# import rospy

if __name__ == "__main__":
    cam = Vision(True)
    pr = Procedure()
    pr.load("assets/class/coco.txt",
            "assets/data/nice.pt")
    try:
        while True:
            frame = cam.read(480, True)
            detect = pr.predict(frame)
            pr.draw(frame, detect)
            cam.show(frame, "frame")
            cam.wait(1)
    except RuntimeError:
        pass

    # try:
    #     rospy.init_node("cat_fur", anonymous=True)
    #     rate = rospy.Rate(10)
    #     while not rospy.is_shutdown():
    #         frame = cam.read(frame_size=480, show_fps=True)
    #         detect = rt.get(frame=frame)
    #         print(f"detect : {detect}")
    #         rt.draw(frame=frame, detection=detect)
    #         cam.show(frame, "frame")
    #         cam.wait(1)
    # except rospy.ROSInterruptException:
    #     pass
