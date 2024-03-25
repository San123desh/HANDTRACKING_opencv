from ultralytics import YOLO

model = YOLO("yolov8m.pt")

model.predict(source = "1.jpeg", show=True, save = True, conf = 0.5)