import cv2
import sys

def detect_faces(image_path):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not find or load image {image_path}")
        return

    # Convert to grayscale for the detector
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    # scaleFactor: Parameter specifying how much the image size is reduced at each image scale
    # minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(f"Found {len(faces)} face(s).")

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print(f"Face located at: X: {x}, Y: {y}, Width: {w}, Height: {h}")

    # Display the output
    cv2.imshow('Face Detection', image)
    print("Press any key on the image window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # To run: python script_name.py path_to_your_image.jpg
    if len(sys.argv) > 1:
        detect_faces(sys.argv[1])
    else:
        print("Usage: python script_name.py <image_path>")