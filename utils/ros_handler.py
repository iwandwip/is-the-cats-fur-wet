#!/usr/bin/python

import sys
import os
import rospy
import rosparam
from std_msgs.msg import Int8MultiArray, MultiArrayDimension
from std_msgs.msg import Int16MultiArray, Int32MultiArray
from std_msgs.msg import Float32MultiArray

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import numpy as np
import cv2
import time

import roslib

# MACROS    
KF_FOCAL_LENS = 347.10
KF_REAL_BALL_WIDTH = 14.6
MIN_RADIUS_OF_BALL = 5


class RosHandler:
    # static
    bridge = CvBridge()

    ballFilter = rospy.Publisher("ball/coordinate_filter", Float32MultiArray, queue_size=10)
    ballCoordinate = rospy.Publisher("ball/coordinate", Int16MultiArray, queue_size=10)
    ballState = rospy.Publisher("ball/ball_state", Int8MultiArray, queue_size=10)
    frameSize = rospy.Publisher("frame/frame_size", Int32MultiArray, queue_size=10)

    # rate = rospy.Rate(30)

    # ball
    ball_last_pos_x = -1
    ball_last_pos_y = -1
    
    @staticmethod
    def imgMsg2Frame(data):
        frame = []
        try:
            frame = RosHandler.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        return frame
    
    @staticmethod
    def compressedImgMsg2Frame(data):
        frame = []
        try:
            frame = RosHandler.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        return frame

    @classmethod
    def ball2ros(self, data, shape):
        try:
            x_filter, y_filter, distance, radius = 0, 0, 0, 0
            flag, pos_y, pos_x, pos_kick = 0, -1, -1, 0
            # if data != {}:
                # # print(data["size"])
                # if data["size"] > MIN_RADIUS_OF_BALL:
                #     x_filter = (data["x_pos"] / shape[1]) * 2 - 1
                #     y_filter = (data["y_pos"] / shape[0]) * 2 - 1
                #     distance = (KF_REAL_BALL_WIDTH / KF_FOCAL_LENS) * data["size"]
                #     flag = 1
                # else:
                #     flag = 0
                # if flag:
                #     pos_y = 2 if data["y_pos"] < 85 else 1 if data["y_pos"] > shape[0] - 85 else 0 
                #     pos_x = 2 if data["x_pos"] < 100 else 1 if data["x_pos"] > shape[1] - 100 else 0
                #     pos_kick = 0 if data["x_pos"] < (shape[1] // 2) else 1
                #     RosHandler.ball_last_pos_y = pos_y
                #     RosHandler.ball_last_pos_x = pos_x

                #     coordinate = Float32MultiArray()
                #     position = Int16MultiArray()
                #     position.layout.dim.append(MultiArrayDimension())
                #     position.layout.dim[0].size = 3
                #     position.layout.dim[0].stride = 1
                #     coordinate.data = [x_filter, y_filter, distance]
                #     position.data = [int(data["x_pos"]), int(data["y_pos"]), int(data["size"] // 2)]

                #     RosHandler.ballFilter.publish(coordinate)
                #     RosHandler.ballCoordinate.publish(position)

                # else:
                #     pos_y = -1
                #     pos_x = -1

                # state = Int8MultiArray()
                # state.data = [pos_x, pos_y, pos_kick,
                #               RosHandler.ball_last_pos_x,
                #               RosHandler.ball_last_pos_y,
                #               flag]
                # RosHandler.ballState.publish(state)
            # print(data["size"])
            if data != {}:
                x_filter = (data["x_pos"] / shape[1]) * 2 - 1
                y_filter = (data["y_pos"] / shape[0]) * 2 - 1
                distance = (KF_REAL_BALL_WIDTH / KF_FOCAL_LENS) * data["size"]
                flag = 1
            else:
                flag = 0
            if flag:
                pos_y = 2 if data["y_pos"] < 85 else 1 if data["y_pos"] > shape[0] - 85 else 0 
                pos_x = 2 if data["x_pos"] < 100 else 1 if data["x_pos"] > shape[1] - 100 else 0
                pos_kick = 0 if data["x_pos"] < (shape[1] // 2) else 1
                RosHandler.ball_last_pos_y = pos_y
                RosHandler.ball_last_pos_x = pos_x

                coordinate = Float32MultiArray()
                position = Int16MultiArray()
                position.layout.dim.append(MultiArrayDimension())
                position.layout.dim[0].size = 3
                position.layout.dim[0].stride = 1
                coordinate.data = [x_filter, y_filter, distance]
                position.data = [int(data["x_pos"]), int(data["y_pos"]), int(data["size"] // 2)]

                RosHandler.ballFilter.publish(coordinate)
                RosHandler.ballCoordinate.publish(position)

            else:
                pos_y = -1
                pos_x = -1

            state = Int8MultiArray()
            state.data = [pos_x, pos_y, pos_kick,
                          RosHandler.ball_last_pos_x,
                          RosHandler.ball_last_pos_y,
                          flag]
            
            frame_size = Int32MultiArray()
            frame_size.data = [shape[0], shape[1]]

            RosHandler.frameSize.publish(frame_size)
            RosHandler.ballState.publish(state)
        except KeyError as e:
            pass