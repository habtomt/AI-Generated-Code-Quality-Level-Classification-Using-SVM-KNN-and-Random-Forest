"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_000.txt
Run      : 3
"""

# Import the required OpenCV library for face detection and processing
import cv2

# Load the pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the image to detect faces
def detect_faces(image_path):
    try:
        # Open the image using OpenCV
        img = cv2.imread(image_path)
        
        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Display the original and face-detected images
        cv2.imshow('Original Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage
detect_faces('path_to_your_image.jpg')