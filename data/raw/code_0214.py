import torch
from torchvision import models, transforms
from PIL import Image, ImageDraw, ImageFont
import requests

def object_detection_and_categorization(image_path):
    # Load a pre-trained Faster R-CNN model
    model = models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
    model.eval()

    # COCO Class labels
    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    # Load and transform the image
    img = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([transforms.ToTensor()])
    img_tensor = transform(img)

    # Perform inference
    with torch.no_grad():
        prediction = model([img_tensor])

    # Draw results
    draw = ImageDraw.Draw(img)
    
    # Filter predictions by confidence score (e.g., > 0.8)
    for i in range(len(prediction[0]['scores'])):
        score = prediction[0]['scores'][i].item()
        if score > 0.8:
            box = prediction[0]['boxes'][i].detach().numpy()
            label_idx = prediction[0]['labels'][i].item()
            label = COCO_INSTANCE_CATEGORY_NAMES[label_idx]
            
            # Draw rectangle
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
            # Draw label
            draw.text((box[0], box[1]), f"{label}: {score:.2f}", fill="red")
            
            print(f"Detected: {label} (Confidence: {score:.2f}) at {box}")

    img.show()
    img.save("detected_objects.jpg")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        object_detection_and_categorization(sys.argv[1])
    else:
        print("Usage: python script.py <image_path>")