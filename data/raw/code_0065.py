#!/usr/bin/env python3

import cv2
import math
import time
import numpy as np


DEST_LAT = 41.015137
DEST_LON = 28.979530  # Istanbul (example destination)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def bearing(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    y = math.sin(dlon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlon)

    brng = math.degrees(math.atan2(y, x))
    return (brng + 360) % 360


def simulate_gps(lat, lon, dest_lat, dest_lon):
    lat += (dest_lat - lat) * 0.0005
    lon += (dest_lon - lon) * 0.0005
    return lat, lon


def draw_arrow(frame, angle):
    h, w, _ = frame.shape
    center = (w // 2, h // 2)

    length = 100

    rad = math.radians(angle)

    end_x = int(center[0] + length * math.sin(rad))
    end_y = int(center[1] - length * math.cos(rad))

    cv2.arrowedLine(frame, center, (end_x, end_y), (0, 255, 0), 5, tipLength=0.3)

    cv2.putText(frame, f"Bearing: {int(angle)} deg", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def main():
    cap = cv2.VideoCapture(0)

    lat, lon = 41.0082, 28.9784  # start (Istanbul)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        lat, lon = simulate_gps(lat, lon, DEST_LAT, DEST_LON)

        brng = bearing(lat, lon, DEST_LAT, DEST_LON)
        dist = haversine(lat, lon, DEST_LAT, DEST_LON)

        draw_arrow(frame, brng)

        cv2.putText(frame, f"Distance: {dist:.2f} km", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("AR Navigation", frame)

        if cv2.waitKey(30) & 0xFF == 27:
            break

        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()