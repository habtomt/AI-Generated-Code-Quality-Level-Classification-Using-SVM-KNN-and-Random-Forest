"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_000.txt
Run      : 1
"""

import cv2

# Load the pre-trained Haar Cascade classifier XML file
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)

        # Check if image is loaded fine
        if image is None:
            print('Error opening image!')
            return

        # Convert the image to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        print(f"Found {len(faces)} faces!")

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show the output image
        cv2.imshow('Faces found', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
image_path = 'path_to_your_image.jpg'
detect_faces(image_path)