#!/usr/bin/env python3

import cv2
import sys
import pytesseract


def detect_license_plates(frame, plate_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))

    results = []

    for (x, y, w, h) in plates:
        roi = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 7')
        cleaned = "".join(c for c in text if c.isalnum())

        if cleaned:
            results.append((cleaned, (x, y, w, h)))

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, cleaned, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame, results


def process_image(image_path, plate_cascade):
    frame = cv2.imread(image_path)
    if frame is None:
        print("Image not found")
        return

    processed, results = detect_license_plates(frame, plate_cascade)

    print(results)
    cv2.imshow("License Plate Detection", processed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_video(video_path, plate_cascade):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed, results = detect_license_plates(frame, plate_cascade)

        if results:
            print(results)

        cv2.imshow("License Plate Detection", processed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    if len(sys.argv) < 3:
        print("Usage: python license_plate.py <image|video> <path>")
        sys.exit(1)

    mode = sys.argv[1]
    path = sys.argv[2]

    cascade_path = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
    plate_cascade = cv2.CascadeClassifier(cascade_path)

    if mode == "image":
        process_image(path, plate_cascade)
    elif mode == "video":
        process_video(path, plate_cascade)
    else:
        print("Invalid mode. Use 'image' or 'video'.")


if __name__ == "__main__":
    main()