import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO


model = YOLO('best.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture("3.mp4")


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
# print(class_list)
count = 0


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


while True:
    ret, frame = cap.read()
    count += 1
    if count % 3 != 0:
        continue

    frame = resizeFrame(frame, 240)

    results = model.predict(frame)

    # print(results)
    a = results[0].boxes.boxes
    # print(a)
    px = pd.DataFrame(a).astype("float")
    # print(px)
    for index, row in px.iterrows():
        #        print(row)

        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        print(str(c))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(c), (x1, y1),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
    # cv2.imwrite(
    #     r"C:\Users\Brainless\Downloads\yolov8custom-obj-count-main\yolov8custom-obj-count-main\kucing.mkv", frame)
    cv2.imshow("Kucing", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
