import cv2
import numpy as np
import sys

def segment_image(image_path, k_clusters=5):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return

    # Convert BGR to RGB for processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to a 2D array of pixels (N, 3)
    pixel_values = image_rgb.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Define stopping criteria (100 iterations or epsilon 0.2)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Perform K-Means Clustering to segment regions by color
    _, labels, (centers) = cv2.kmeans(pixel_values, k_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)
    
    # Map pixels to their center color
    segmented_data = centers[labels.flatten()]
    
    # Reshape back to the original image dimensions
    segmented_image = segmented_data.reshape((image_rgb.shape))

    # Display results
    cv2.imshow('Original Image', image)
    cv2.imshow(f'Segmented Image (K={k_clusters})', cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
    
    print(f"Image divided into {k_clusters} color-based regions.")
    print("Press any key to close the windows.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        img_path = sys.argv[1]
        clusters = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        segment_image(img_path, clusters)
    else:
        print("Usage: python script.py <image_path> [number_of_regions]")