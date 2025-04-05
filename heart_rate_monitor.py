import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Initialize Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

intensity_values = []
sampling_time = 7  # Seconds to capture data
fps = 30  # Frames per second (adjust based on your webcam)
total_frames = sampling_time * fps

print("Place your fingertip over the camera and stay still...")

# Start capturing
start_time = time.time()
while len(intensity_values) < total_frames:
    ret, frame = cap.read()
    if not ret:
        print("Error: Frame not captured.")
        break

    # Convert frame to HSV and extract Red channel intensity
    roi = frame[100:300, 200:400]  # Define Region of Interest (ROI)
    red_channel = roi[:, :, 2]
    avg_intensity = np.mean(red_channel)
    intensity_values.append(avg_intensity)

    # Show real-time feedback
    cv2.rectangle(frame, (200, 100), (400, 300), (0, 255, 0), 2)
    cv2.putText(frame, "Place Finger Here", (210, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Finger Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Convert to NumPy array
intensity_values = np.array(intensity_values)

# Smooth the data
window_size = 5
smoothed_values = np.convolve(intensity_values, np.ones(window_size)/window_size, mode='valid')

# Detect peaks
sampling_rate = fps  # Approximate sampling rate
peaks, _ = find_peaks(smoothed_values, distance=sampling_rate/3, height=np.mean(smoothed_values) * 0.9)

# Calculate BPM
num_beats = len(peaks)
bpm = (num_beats / sampling_time) * 60

# Plot the detected heart rate signal
plt.figure(figsize=(10, 5))
plt.plot(smoothed_values, label="Smoothed Intensity", color='blue')
plt.plot(peaks, smoothed_values[peaks], "ro", label="Detected Peaks")  # Mark peaks
plt.title(f"Estimated Heart Rate: {bpm:.2f} BPM")
plt.xlabel("Time (frames)")
plt.ylabel("Red Intensity")
plt.legend()
plt.show()

print(f"Estimated Heart Rate: {bpm:.2f} BPM")
