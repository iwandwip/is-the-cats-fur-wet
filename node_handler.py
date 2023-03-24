import rospy


class NodeHandler(object):
    def __init__(self):
        rospy.init_node("cat-fur", anonymous=True)
