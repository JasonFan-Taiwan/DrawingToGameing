import cv2
import numpy as np

class YoloDetector:
    def __init__(self, config_path, weights_path, classes_path):
        # Load YOLO
        self.net = cv2.dnn.readNet(weights_path, config_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Load classes
        with open(classes_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect_objects(self, image):
        height, width, _ = image.shape
        # Preparing the image for YOLO
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Information to show on the screen
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non-max suppression to reduce overlapping boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        detected_objects = []
        for i in range(len(boxes)):
            if i in indexes:
                label = str(self.classes[class_ids[i]])
                detected_objects.append((label, boxes[i]))

        return detected_objects

# Usage:
# yolo = YoloDetector('yolov3.cfg', 'yolov3.weights', 'coco.names')
# image = cv2.imread('image.jpg')
# detections = yolo.detect_objects(image)