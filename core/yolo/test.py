import cv2
import torch
import numpy as np

model_path = "yolov5s.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
