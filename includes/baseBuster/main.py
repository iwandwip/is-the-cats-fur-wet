import cv2
import torch
import numpy as np


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


model = torch.hub.load('ultralytics/yolov5', 'custom',
                       'best.pt', force_reload=True)

cap = cv2.VideoCapture("cat.mp4")
while True:
    ret, frame = cap.read()
    frame = resizeFrame(frame, 350)
    if not ret:
        break

    width = frame.shape[1]
    height = frame.shape[0]
    results = model(frame)

    pred = results.pred[0]  # ambil hasil prediksi pada frame pertama
    boxes = pred[:, :4].cpu().numpy()  # ambil koordinat bounding box
    labels = pred[:, -1].cpu().numpy()  # ambil label
    confidences = pred[:, 4].cpu().numpy()  # ambil confidence

    try:
        print(
            f"label = {int(labels)} | conf = {float(confidences)} | box = {list(boxes[0])}")
        # frame = np.squeeze(results.render())

        for box, label, confidence in zip(boxes, labels, confidences):
            if confidence > 0.3:
                x1, y1, x2, y2 = box
                x_center = int((box[0] + box[2]) / 2 * width)
                y_center = int((box[1] + box[3]) / 2 * height)
                box_width = int((box[2] - box[0]) * width)
                box_height = int((box[3] - box[1]) * height)

                print(
                    f"x: {x_center} | y: {y_center} | w: {box_width} | h: {box_height}")

                cv2.rectangle(frame, (int(x1), int(y1)),
                              (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, str(label), (int(x1), int(y1)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    except TypeError:
        pass

    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
