import re

def simulate_alpr_process(image_path):
    """
    Simulates the Automated License Plate Recognition (ALPR) pipeline:
    1. Image Preprocessing (Grayscale/Noise Reduction)
    2. Plate Localization (Finding the rectangle)
    3. Character Segmentation
    4. Optical Character Recognition (OCR)
    """
    
    # In a real-world scenario, you would use libraries like:
    # cv2 (OpenCV) for image processing
    # pytesseract for OCR
    
    print(f"[*] Accessing image: {image_path}")
    print("[*] Performing localized edge detection...")
    print("[*] Extracting character contours...")

    # Simulated OCR output from a vehicle image
    mock_ocr_results = {
        "car_1.jpg": "ABC-1234",
        "car_2.png": "KL-08-CC-5678",
        "car_3.jpg": "PLATE-77",
    }

    raw_plate = mock_ocr_results.get(image_path.split('/')[-1], "UNKNOWN")
    
    # Cleaning the detected text using Regex (common for toll/parking logic)
    clean_plate = re.sub(r'[^A-Z0-9-]', '', raw_plate.upper())
    
    return clean_plate

def process_parking_entry(plate_number):
    """
    Business logic for a parking management system.
    """
    authorized_vehicles = ["ABC-1234", "PLATE-77"]
    
    print(f"\n[SYSTEM] Processing Plate: {plate_number}")
    
    if plate_number in authorized_vehicles:
        print("Result: ACCESS GRANTED - Subscription Active")
    elif plate_number == "UNKNOWN":
        print("Result: ERROR - Could not read plate clearly")
    else:
        print("Result: ACCESS DENIED - Visitor Ticket Required")

def main():
    # Mock file paths representing frames from a security camera
    camera_frames = [
        "images/car_1.jpg", 
        "images/car_2.png", 
        "images/unknown_vehicle.jpg"
    ]

    print("--- ALPR Security System Initialized ---")
    
    for frame in camera_frames:
        detected_plate = simulate_alpr_process(frame)
        process_parking_entry(detected_plate)

if __name__ == "__main__":
    main()