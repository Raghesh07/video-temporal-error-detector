import cv2

cap = cv2.VideoCapture("input_video.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
expected_interval = 1.0 / fps if fps > 0 else 0

frames = []
timestamps = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
    frames.append(frame)
    timestamps.append(timestamp)

cap.release()

print("FPS:", fps)
print("Total frames:", len(frames))
print("First 5 timestamps:", timestamps[:5])
import numpy as np
import csv

# ---------- FRAME DROP DETECTION ----------
frame_labels = ["Normal"]

for i in range(1, len(timestamps)):
    delta = timestamps[i] - timestamps[i - 1]

    if expected_interval > 0 and delta > expected_interval * 1.5:
        frame_labels.append("Frame Drop")
    else:
        frame_labels.append("Normal")

print("Frame Drop Count:", frame_labels.count("Frame Drop"))

# ---------- FRAME MERGE DETECTION ----------
gray_frames = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

motion_scores = [0]
for i in range(1, len(gray_frames)):
    diff = cv2.absdiff(gray_frames[i], gray_frames[i - 1])
    motion_scores.append(np.mean(diff))

avg_motion = np.mean(motion_scores)

for i in range(len(frame_labels)):
    if frame_labels[i] == "Normal" and motion_scores[i] < avg_motion * 0.4:
        frame_labels[i] = "Frame Merge"

print("Frame Merge Count:", frame_labels.count("Frame Merge"))

# ---------- VISUAL OUTPUT ----------
h, w, _ = frames[0].shape

out = cv2.VideoWriter(
    "output_annotated.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (w, h)
)

for i, frame in enumerate(frames):
    label = frame_labels[i]

    color = (0, 255, 0)
    if label == "Frame Drop":
        color = (0, 0, 255)
    elif label == "Frame Merge":
        color = (0, 255, 255)

    cv2.putText(frame, label, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    out.write(frame)

out.release()
print("Annotated video saved as output_annotated.mp4")

# ---------- CSV REPORT ----------
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Frame Index", "Timestamp", "Label"])
    for i in range(len(frame_labels)):
        writer.writerow([i, timestamps[i], frame_labels[i]])

print("Frame-level report saved as results.csv")