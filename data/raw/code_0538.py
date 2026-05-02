"""
Auto-generated Python code
Scenario : OCR (Optical Character Recognition)
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import os

# Load the license plate detection model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load the license plate recognition model
plate_recognizer = cv2.face.LBPHFaceRecognizer_create()
plate_recognizer.read("license_plate_recognizer.yml")

# Load the list of known license plates
known_plates = {}
with open("known_plates.txt", "r") as f:
    for line in f:
        plate, label = line.strip().split(",")
        known_plates[plate] = label

# Function to detect license plates
def detect_license_plates(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect objects using YOLO
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    # Draw rectangles around detected objects
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Class 0 is the license plate class
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Non-maximum suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Draw rectangles around detected license plates
    if len(indices) > 0:
        for i in indices:
            i = i[0]
            box = boxes[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Extract the license plate region of interest
            roi = img[y:y + h, x:x + w]
            
            # Convert the ROI to grayscale
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to the ROI
            _, thresh = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Recognize the license plate using Tesseract
            try:
                text = pytesseract.image_to_string(thresh, config='--psm 11')
                text = text.strip()
                return text
            except Exception as e:
                print(f"Error recognizing license plate: {e}")
                return None
    return None

# Function to recognize license plates in videos
def recognize_license_plates_in_videos(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        text = detect_license_plates(frame)
        if text is not None:
            print(f"License plate detected: {text}")
            # Check if the license plate is known
            label = known_plates.get(text)
            if label is not None:
                print(f"Known license plate: {label}")
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    # Recognize license plates in images
    image_path = "image.jpg"
    text = detect_license_plates(image_path)
    if text is not None:
        print(f"License plate detected: {text}")

    # Recognize license plates in videos
    video_path = "video.mp4"
    recognize_license_plates_in_videos(video_path)