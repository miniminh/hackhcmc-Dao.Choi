from ultralytics import YOLO
from PIL import Image

MODEL_PATH = 'weights/yolov9c.pt'
model = YOLO(MODEL_PATH)
    
def run_batch(images):
    results = model(images)  # return a list of Results objects

    # Process results list
    for i, result in enumerate(results):
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.save(filename=f'result/image_{i}.jpg')  # save to disk
    return results