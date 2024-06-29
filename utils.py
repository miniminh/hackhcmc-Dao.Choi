import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO

MODEL_PATH = 'weights/best.pt'

model = YOLO(MODEL_PATH)
    
name = model.names

def plot_results(image_path, results, target_classes, output_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB (OpenCV uses BGR by default)

    # Iterate through each result in the results list
    for result in results:
        boxes = result.boxes.xyxy
        class_ids = result.boxes.cls
        class_probs = result.boxes.conf

        # Iterate through each box, class_id, and probability
        for box, class_id, prob in zip(boxes, class_ids, class_probs):
            if class_id in target_classes:
                # Extract box coordinates
                x1, y1, x2, y2 = box

                # Convert coordinates to integers
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                tensor_index = torch.tensor(class_id)
                id = int(tensor_index.item())

                # Draw rectangle and text on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw rectangle with blue color (BGR)
                class_name = f'{name[id]}'  # Replace with actual class names if available
                cv2.putText(image, f'{class_name} {prob:.2f}', (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    # Save the annotated image
    # output_path = 'annotated_' + image_path
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))