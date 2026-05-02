"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_000.txt
Run      : 2
"""

# Import necessary libraries
import cv2
import numpy as np

# Load the CascadeClassifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in an image
def detect_faces(image_path):
    """
    Detects faces in a given image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        A list of rectangles representing the detected faces.
    """
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        return faces

    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to draw rectangles around detected faces
def draw_faces(image, faces):
    """
    Draws rectangles around detected faces in an image.

    Args:
        image (numpy.ndarray): The input image.
        faces (list): A list of rectangles representing the detected faces.
    """
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Main function
def main():
    # Specify the path to the input image
    image_path = "input_image.jpg"

    # Detect faces in the image
    faces = detect_faces(image_path)

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Draw rectangles around detected faces
    draw_faces(image, faces)

    # Display the output image
    cv2.imshow("Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the output image
    cv2.imwrite("output_image.jpg", image)

# Run the main function
if __name__ == "__main__":
    main()