"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_001.txt
Run      : 1
"""

# Import required libraries
import cv2
import pytesseract
import numpy as np
import imutils

# Specify Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the YOLO configuration and weights files
model_cfg = 'license-plate-yolov4.cfg'
model_weights = 'license-plate-yolov4.weights'

# Initialize the YOLO model
net = cv2.dnn.readNetFromDarknet(model_cfg, model_weights)
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def detect_and_read_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image
    image = imutils.resize(image, width=500)

    # Prepare the image for YOLO
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Run the detection
    detections = net.forward(output_layers)

    # Initialize variables
    boxes = []
    confidences = []

    # Parse YOLO output
    for detection in detections:
        for object_detection in detection:
            scores = object_detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Consider only detections with high confidence
            if confidence > 0.5:
                center_x = int(object_detection[0] * width)
                center_y = int(object_detection[1] * height)
                w = int(object_detection[2] * width)
                h = int(object_detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))

    # Apply Non-max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, w, h = box

        # Crop the license plate region
        license_plate_region = image[y:y + h, x:x + w]

        # Use Tesseract to read the license plate
        try:
            text = pytesseract.image_to_string(license_plate_region, config='--psm 8')
            print(f"Detected License Plate: {text.strip()}")
        except Exception as e:
            print(f"Error reading license plate: {e}")

        # Optionally, draw bounding boxes on the original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the final image (optional)
    cv2.imshow("License Plate Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to image
image_path = 'path_to_vehicle_image.jpg'
detect_and_read_plate(image_path)