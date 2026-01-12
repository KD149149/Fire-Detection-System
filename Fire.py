#
# #Fire Detection Robot
#
# import cv2
# import numpy as np
# import pandas as pd
# from datetime import datetime
#
# # -----------------------------
# # Settings
# # -----------------------------
# video_file = "fire_detection_output.mp4"
# excel_file = "fire_report.xlsx"
# location_name = "Location A"  # Replace with real location if needed
#
# # Create empty DataFrame for fire report
# df = pd.DataFrame(columns=["Timestamp", "Location", "Frequency", "Event"])
#
# # Initialize video capture
# cap = cv2.VideoCapture(0)  # 0 = webcam
#
# # Video writer for MP4
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(video_file, fourcc, 20.0, (640, 480))
#
# # Fire detection parameters
# min_area = 500  # Minimum contour area to reduce false positives
# frequency_counter = 0
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     frame = cv2.resize(frame, (640, 480))
#
#     # Convert to HSV for color detection
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#     # High-intensity fire color range (bright orange-red)
#     lower_fire = np.array([0, 150, 200])
#     upper_fire = np.array([35, 255, 255])
#
#     mask = cv2.inRange(hsv, lower_fire, upper_fire)
#
#     # Find contours of fire regions
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     fire_detected = False
#     max_area = 0
#
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > min_area:
#             x, y, w, h = cv2.boundingRect(cnt)
#             # Intensity = area (can be mapped to extreme scale)
#             intensity = min(int(area / 1000), 100)  # scale 0-100
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#             cv2.putText(frame, f"FIRE {intensity}%", (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
#             fire_detected = True
#             max_area = max(max_area, intensity)
#
#     # Log fire event
#     if fire_detected:
#         frequency_counter += 1
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         df = pd.concat([df, pd.DataFrame([[timestamp, location_name, max_area, "Fire detected"]],
#                                          columns=df.columns)], ignore_index=True)
#
#     # Show live frame
#     cv2.imshow("Fire Detection", frame)
#
#     # Save frame to video
#     out.write(frame)
#
#     # Stop on 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Save Excel report
# df.to_excel(excel_file, index=False)
#
# # Release resources
# cap.release()
# out.release()
# cv2.destroyAllWindows()
#
# print(f"Video saved as '{video_file}'")
# print(f"Fire report saved as '{excel_file}'")


import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

# ---------------------------
# Configuration
# ---------------------------
video_folder = "fire_videos"
report_file = "fire_report.xlsx"
location_name = "Site_A"  # replace with your location

# Ensure video folder exists
os.makedirs(video_folder, exist_ok=True)

# Excel report setup
columns = ["Date", "Time", "Location", "Fire Detected", "Frequency"]
df = pd.DataFrame(columns=columns)

# ---------------------------
# Video capture & output
# ---------------------------
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Create timestamped video filename
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
video_file = os.path.join(video_folder, f"fire_{timestamp_str}.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 format
out = cv2.VideoWriter(video_file, fourcc, 20.0, (frame_width, frame_height))

# ---------------------------
# Fire detection loop
# ---------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV to detect orange flames
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define fire color range (high intensity orange/red)
    lower_fire = np.array([5, 150, 150])
    upper_fire = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    # Remove noise
    mask = cv2.medianBlur(mask, 5)

    # Find contours of fire
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fire_detected = False
    max_intensity = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # only significant fire
            x, y, w, h = cv2.boundingRect(cnt)
            fire_region = mask[y:y + h, x:x + w]
            intensity = np.mean(fire_region) / 255  # normalized fire intensity
            max_intensity = max(max_intensity, intensity)

            # Draw bounding box with intensity label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"FIRE {intensity:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            fire_detected = True

    # Log to Excel dataframe
    if fire_detected:
        now = datetime.now()
        df = pd.concat([df, pd.DataFrame(
            [[now.date(), now.time().strftime("%H:%M:%S"), location_name, "Yes", round(max_intensity, 2)]],
            columns=columns)], ignore_index=True)

    # Show live detection
    cv2.imshow("Fire Detection", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------------------
# Save Excel report & release resources
# ---------------------------
df.to_excel(report_file, index=False)
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved: {video_file}")
print(f"Report saved: {report_file}")
