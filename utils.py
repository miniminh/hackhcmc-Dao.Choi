import cv2
import numpy as np
from PIL import Image
import torch
import colorsys
from ultralytics import YOLO

MODEL_PATH = 'weights/best.pt'

model = YOLO(MODEL_PATH)
    
name = model.names

def generate_colors(num_classes):
    hsv_colors = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    rgb_colors = [tuple(int(255 * x) for x in colorsys.hsv_to_rgb(*color)) for color in hsv_colors]
    return rgb_colors

# Generate colors for all classes
colors = generate_colors(len(name))

# Function to plot results and highlight logo
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

                # Get class index from tensor
                tensor_index = torch.tensor(class_id)
                id = int(tensor_index.item())

                # Get color for current class
                color = colors[id]

                # Draw rectangle and text on the image with class-specific color
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)  # Draw rectangle with class color
                class_name = f'{name[id]}'  # Replace with actual class names if available
                cv2.putText(image, f'{class_name} {prob:.2f}', (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Save the annotated image
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def is_inside_soft(bbox1, bbox2, margin_factor=0.2):
    """
    Check if bbox1 is inside bbox2 with a soft margin.
    
    Args:
    - bbox1 (tuple): Bounding box coordinates (x_min, y_min, x_max, y_max).
    - bbox2 (tuple): Bounding box coordinates (x_min, y_min, x_max, y_max).
    - margin_factor (float): Margin factor to allow for soft containment (default is 0.1).

    Returns:
    - bool: True if bbox1 is inside bbox2 with the soft margin, False otherwise.
    """
    # Extract coordinates
    x_min1, y_min1, x_max1, y_max1 = bbox1
    x_min2, y_min2, x_max2, y_max2 = bbox2
    
    # Calculate margins
    width_margin = (x_max2 - x_min2) * margin_factor
    height_margin = (y_max2 - y_min2) * margin_factor
    
    # Check if bbox1 is inside bbox2 with the soft margin
    if (x_min1 >= x_min2 - width_margin and
        y_min1 >= y_min2 - height_margin and
        x_max1 <= x_max2 + width_margin and
        y_max1 <= y_max2 + height_margin):
        return True
    else:
        return False
