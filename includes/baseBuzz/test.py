import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO


def frame(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        # print(colorsBGR)


def resizeFrame(image, width=None, height=None, interpolasi=cv2.INTER_AREA):
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
    resized = cv2.resize(image, dim, interpolation=interpolasi)
    return resized


model = YOLO('best.pt')
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', frame)

cap = cv2.VideoCapture("3.mp4")
class_list = open("coco.txt", "r").read().split("\n")

while True:
    ret, frame = cap.read()
    frame = resizeFrame(frame, 240)
    results = model.predict(frame)
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    x1, x2, y1, y2, conf = 0, 0, 0, 0, 0
    ft = cv2.FONT_HERSHEY_COMPLEX
    for index, row in px.iterrows():
        x1, x2 = int(row[0]), int(row[2])
        y1, y2 = int(row[1]), int(row[3])
        conf = row[4]
        c = class_list[int(row[5])]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(c), (x1, y1), ft, 0.5, (255, 0, 0), 1)
    print("x: {}, y: {}, width: {}, height: {}, conf: {}".format(
        (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, conf))
    center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
    cv2.circle(frame, center, 2, (0, 0, 255), -1)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
