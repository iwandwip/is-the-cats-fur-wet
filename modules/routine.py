import sys
import os

# from ultralytics import YOLO as ul
import pandas as pd
import numpy as np
import torch
import cv2
import time


class ImgRex: # 3
    def __init__(self):
        pass

    def __map(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) // (inMax - inMin) + outMin

    def load(self, weight_path, cfg, classes):
        self.classes = None
        with open(classes, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.colors = np.random.uniform(
            0, 255, size=(len(self.classes), 3))  # optional
        # self.net = cv2.dnn.readNet(weight_path, cfg)
        self.net = cv2.dnn.readNetFromDarknet(cfg, weight_path)
        layer_names = self.net.getLayerNames()
        # self.output_layers = [layer_names[i - 1]
        #                       for i in self.net.getUnconnectedOutLayers()]
        self.output_layers = self.net.getUnconnectedOutLayersNames()

    def dettect(self, frame):
        blob = cv2.dnn.blobFromImage(
            frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        height, width, ch = frame.shape
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = [np.argmax(detection[5:])
                     for out in outs for detection in out]
        confidences = [detection[np.argmax(detection[5:]) + 5]
                       for out in outs for detection in out]
        boxes = [[int(center_x - w / 2), int(center_y - h / 2), int(detection[2] * width), int(detection[3] * height)]
                 for out in outs for detection in out
                 if detection[np.argmax(detection[5:]) + 5] > 0.5
                 for center_x, center_y, w, h in [((detection[0] * width), (detection[1] * height),
                                                  (detection[2] * width), (detection[3] * height))]]
        if len(boxes) > 0:
            indexes = cv2.dnn.NMSBoxes(
                boxes, confidences, 0.5, 0.4)  # 0.4 changeable
            font = cv2.FONT_HERSHEY_PLAIN
            values = {}
            for i in indexes.flatten():
                label = str(self.classes[class_ids[i]])
                x, y, w, h = boxes[i]
                temp = {
                    "class": label,
                    "confidence": confidences[i],
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "center": 0,
                    "color": self.colors[class_ids[i]]
                }
                values.update(temp)
            return values

    @staticmethod
    def draw(frame, detection):
        if detection is not []:
            for idx in detection:
                color = idx["color"]
                cv2.rectangle(
                    frame, (idx["x"], idx["y"]), (idx["x"] + idx["width"], idx["y"] + idx["height"]), color, 2)
                tl = round(0.002 * (frame.shape[0] + frame.shape[1]) / 2) + 1
                c1, c2 = (int(idx["x"]), int(idx["y"])), (int(
                    idx["width"]), int(idx["height"]))

                tf = int(max(tl - 1, 1))  # font thickness
                t_size = cv2.getTextSize(
                    idx["class"], 0, fontScale=tl / 3, thickness=tf)[0]
                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

                cv2.rectangle(frame, c1, c2, color, -1, cv2.LINE_AA)  # filled
                cv2.putText(frame, idx["class"] + " " + str(int(idx["confidence"] * 100)) + "%",
                            (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
                cv2.circle(frame, (
                    int(idx["x"] + int(idx["width"] / 2)), int(idx["y"] + int(idx["height"] / 2))),
                    4, color, -1)
                cv2.putText(frame, str(int(idx["x"] + int(idx["width"] / 2))) + ", " + str(
                    int(idx["y"] + int(idx["height"] / 2))), (
                    int(idx["x"] + int(idx["width"] / 2) + 10),
                    int(idx["y"] + int(idx["height"] / 2) + 10)), cv2.FONT_HERSHEY_PLAIN, tl / 2,
                    [255, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        return frame

    def predict(self, frame):
        blob = cv2.dnn.blobFromImage(
            frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        height, width, ch = frame.shape
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        center = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    center.append([center_x, center_y])
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        values = []
        indexes = cv2.dnn.NMSBoxes(
            boxes, confidences, 0.5, 0.4)  # 0.4 changeable
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                label = str(self.classes[class_ids[i]])
                x, y, w, h = boxes[i]
                temp = {
                    "class": label,
                    "confidence": confidences[i],
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "center": center[i],
                    "color": self.colors[class_ids[i]]
                }
                values.append(temp)
        return values


class ImgBuzz(ImgRex): # 8
    def __init__(self):
        self.classes = None
        self.colors = None
        self.model = None
        self.count = 0

    def load(self, names, weight):
        name = open(names, "r")
        self.classes = name.read().split("\n")
        self.model = ul(weight)
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def predict(self, frame):
        values = []
        # height, width, ch = frame.shape
        results = self.model.predict(frame)
        res = results[0].boxes.boxes
        px = pd.DataFrame(res).astype("float")
        boxes = []
        center = []
        class_ids = []
        confidences = []
        for index, row in px.iterrows():
            confidence = row[4]
            if confidence > 0.5:
                x1, x2 = int(row[0]), int(row[2])
                y1, y2 = int(row[1]), int(row[3])
                # indexes, conf = index, row[4]
                # labels = self.classes[int(row[5])]
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                center.append([int((x1 + x2) / 2), int((y1 + y2) / 2)])
                confidences.append(round(row[4], 2))
                class_ids.append(int(row[5]))
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            temp = {
                "class": str(self.classes[class_ids[i]]),
                "confidence": confidences[i],
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "center": center[i],
                "color": self.colors[class_ids[i]]
            }
            values.append(temp)
        return values


class ImgBuster(ImgRex): # 5
    def __init__(self):
        self.classes = None
        self.colors = None
        self.model = None
        self.count = 0

    def load(self, names, weight):
        name = open(names, "r")
        self.classes = name.read().split("\n")
        self.model = torch.hub.load(
            'ultralytics/yolov5', 'custom', weight, force_reload=True)
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def predict(self, frame):
        width = frame.shape[1]
        height = frame.shape[0]

        values = []
        results = self.model(frame)
        pred = results.pred[0]
        boxes_t = pred[:, :4].cpu().numpy()
        labels_t = pred[:, -1].cpu().numpy()
        confidences_t = pred[:, 4].cpu().numpy()

        boxes = []
        center = []
        class_ids = []
        confidences = []
        try:
            # frame = np.squeeze(results.render())
            for box, label, confidence in zip(boxes_t, labels_t, confidences_t):
                if confidence > 0.5:
                    x1, y1, x2, y2 = box
                    boxes.append([int(x1), int(y1), int(
                        x2) - int(x1), int(y2) - int(y1)])
                    center.append([int((x1 + x2) / 2), int((y1 + y2) / 2)])
                    confidences.append(round(confidence, 2))
                    class_ids.append(int(label))

            for i in range(len(boxes)):
                x, y, w, h = boxes[i]
                temp = {
                    "class": str(self.classes[class_ids[i]]),
                    "confidence": confidences[i],
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "center": center[i],
                    "color": self.colors[class_ids[i]]
                }
                values.append(temp)
        except TypeError:
            pass

        return values
