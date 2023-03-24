import rospy
import main


class NodeHandler(object):
    def __init__(self):
        rospy.init_node("cat-fur", anonymous=True)
        self.rate = rospy.Rate(10)  # 10hz

    def run(self):
        try:
            while not rospy.is_shutdown():
                main.main()
        except rospy.ROSInterruptException:
            pass


if __name__ == "__main__":
    nh = NodeHandler()
    nh.run()
