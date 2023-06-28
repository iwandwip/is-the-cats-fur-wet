import sys
import os

import numpy as np
import cv2
import urllib.request
import time


class Vision:
    def __init__(self, isUsingCam=None, addr=None, index=0):
        # write configuration
        self.frame_count = 0
        self.filenames = None
        self.fourcc = None
        self.out = None

        # get address
        self.cap = None
        if isUsingCam:
            self.cap = cv2.VideoCapture(index)
        else:
            self.cap = cv2.VideoCapture(addr)

        # fps
        self._prev_time = 0
        self._new_time = 0

    def writeConfig(self, name="output.mp4", types="mp4v"):  # XVID -> avi
        self.filenames = name
        self.fourcc = cv2.VideoWriter_fourcc(*types)  # format video
        # filename, format, FPS, frame size
        self.out = cv2.VideoWriter(
            self.filenames, self.fourcc, 15.0, (450, 337))

    def write(self, frame):
        self.out.write(frame)

    def writeImg(self, frame, path="output.png"):
        filename = path
        cv2.imwrite(filename, frame)
        with open(filename, 'ab') as f:
            f.flush()
            os.fsync(f.fileno())

    def resize(self, image, width=None, height=None,
               interpolation=cv2.INTER_AREA):
        dim = None
        w = image.shape[1]
        h = image.shape[0]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(image, dim, interpolation=interpolation)
        return resized

    def __get_fps(self):
        fps = 0.0
        try:
            self._new_time = time.time()
            fps = 1 / (self._new_time - self._prev_time)
            self._prev_time = self._new_time
            fps = 30 if fps > 30 else 0 if fps < 0 else fps
        except ZeroDivisionError as e:
            pass
        return int(fps)

    def blur(self, frame=None, sigma=11):
        return cv2.GaussianBlur(frame, (sigma, sigma), 0)

    def setBrightness(self, frame, value):
        h, s, v = cv2.split(
            cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
        v = np.clip(v.astype(int) + value, 0, 255).astype(np.uint8)
        return cv2.cvtColor(
            cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    def setContrast(self, frame, value):
        alpha = float(131 * (value + 127)) / (127 * (131 - value))
        gamma = 127 * (1 - alpha)
        return cv2.addWeighted(
            frame, alpha, frame, 0, gamma)

    def setBrightnessNcontrast(self, frame, bright=0.0, contr=0.0, beta=0.0):
        return cv2.addWeighted(frame, 1 + float(contr)
                               / 100.0, frame, beta, float(bright))

    def read(self, frame_size=480, show_fps=False):
        try:
            success, frame = self.cap.read()
            if not success:
                raise RuntimeError
            if show_fps:
                try:  # put fps
                    cv2.putText(frame, str(self.__get_fps()) + " fps", (20, 40), 0, 1,
                                [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                except RuntimeError as e:
                    print(e)
            frame = self.resize(frame, frame_size)
            return frame
        except RuntimeError as e:
            print("[INFO] Failed to capture the Frame")

    def readFromUrl(self, url="http://192.168.200.24/cam-hi.jpg", frame_size=480, show_fps=False):
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            if show_fps:
                try:  # put fps
                    cv2.putText(frame, str(self.__get_fps()) + " fps", (20, 40), 0, 1,
                                [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                except RuntimeError as e:
                    print(e)
            frame = self.resize(frame, frame_size)
            return frame
        except RuntimeError as e:
            print("[INFO] Failed to capture the Frame")

    def show(self, frame, winName="frame"):
        cv2.imshow(winName, frame)

    def wait(self, delay):
        return cv2.waitKey(delay)

    def release(self):
        self.cap.release()

    def destroy(self):
        cv2.destroyAllWindows()
