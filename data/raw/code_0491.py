"""
Auto-generated Python code
Scenario : Image Processing
Prompt   : response_004.txt
Run      : 1
"""

import cv2
import numpy as np

def kmeans_segmentation(image_path, K=3):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return
    
    # Convert the image to a 2D array of pixels
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Define criteria, number of clusters(K), and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert center values (which are float) to int
    centers = np.uint8(centers)

    # Map the labels to the colors
    segmented_image = centers[labels.flatten()]

    # Reshape the image back to the original image size
    segmented_image = segmented_image.reshape(image.shape)

    # Display the original and segmented image
    cv2.imshow('Original Image', image)
    cv2.imshow('Segmented Image', segmented_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
kmeans_segmentation('path_to_your_image.jpg', K=3)