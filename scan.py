import cv2
import pandas as pd
from datetime import datetime
import os

# ------------------ LOAD STUDENT DATABASE ------------------
db_file = "students.txt"
students = {}

if os.path.exists(db_file):
    with open(db_file, "r") as f:
        for line in f:
            if "=" in line:
                code, name = line.strip().split("=", 1)
                students[code.strip()] = name.strip()
else:
    print("WARNING: students.txt not found — codes will be saved without names.")

# ------------------ LOAD/CREATE ATTENDANCE CSV ------------------
attendance_file = "attendance.csv"

try:
    df = pd.read_csv(attendance_file)
except:
    df = pd.DataFrame(columns=["Barcode", "Name", "Timestamp"])
    df.to_csv(attendance_file, index=False)

# ------------------ OPENCV BARCODE SCANNER ------------------
detector = cv2.barcode.BarcodeDetector()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Height
print("Camera started. Press Q to quit. Press M for manual entry.")

scanned = set()

def mark_attendance(code):
    """Save attendance record to CSV"""
    name = students.get(code, "Unknown Student")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[+] Marked present: {code} - {name} at {timestamp}")

    global df
    new_row = pd.DataFrame([[code, name, timestamp]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(attendance_file, index=False)

# ------------------ MAIN LOOP ------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Try barcode detection
    ok, decoded_info, decoded_type, points = detector.detectAndDecodeWithType(frame)

    if ok and decoded_info:
        # decoded_info might be a tuple or string - extract the actual barcode value
        if isinstance(decoded_info, tuple):
            code = str(decoded_info[0]).strip() if decoded_info else ""
        else:
            code = str(decoded_info).strip()
        
        if code and code not in scanned:
            scanned.add(code)
            mark_attendance(code)

        # Draw polygon around barcode
        if points is not None and len(points) > 0:
            pts = points[0].astype(int).reshape(-1, 2)
            for i in range(len(pts)):
                cv2.line(frame, tuple(pts[i]), tuple(pts[(i+1) % len(pts)]), (0, 255, 0), 2)

    # Show instructions on screen
    cv2.putText(frame, "Press Q to quit | Press M for manual entry",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Scanning...", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Attendance Scanner", frame)

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):
        break

    # Manual entry
    if key == ord('m'):
        cap.release()
        cv2.destroyAllWindows()
        code = input("Enter barcode manually: ").strip()
        mark_attendance(code)
        cap = cv2.VideoCapture(0)

cap.release()
cv2.destroyAllWindows()
