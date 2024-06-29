from ultralytics import YOLO
from PIL import Image
from utils import plot_results, model

def run_batch(images):
    results = model(images, iou=0.5)  # return a list of Results objects
    return results

def display(images, results, TARGET_CLASS):
    for i, result in enumerate(results):
        images[i].save('temp.png')
        plot_results('temp.png', result, TARGET_CLASS, f'result/image_{i}.jpg')