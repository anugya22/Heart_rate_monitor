Check the working: https://heart-rate-monitoring-v3wi.onrender.com/

# 🩺 Python-Based Health Monitoring System

A lightweight, camera-powered heart rate detection system built in Python, designed for experimental health monitoring purposes. This project is part of a broader embedded system aimed at building a **portable health monitoring band** using ESP32, ADXL345 (step counter), and Telegram Bot integration.



## 📌 Features

- ✅ **Heart Rate Detection** using regular webcam
- 📊 **Red Channel Intensity Analysis** to calculate BPM
- 📉 **Signal Smoothing** with peak detection
- 🔁 **Real-time Visualization**
- 🤖 **Telegram Bot Integration** (optional) to push heart rate data

---

## 🧠 How It Works

1. The webcam captures video frames for **10 seconds**.
2. The Region of Interest (ROI) is isolated where the user places their fingertip.
3. The **red channel intensity** is extracted from each frame.
4. Signal smoothing is applied, and **peaks are detected** to estimate the heart rate.
5. Optionally, the BPM value can be sent to a **Telegram bot** using Python's `requests` library.

---

## 🛠️ Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- SciPy
- Matplotlib
- Requests (for Telegram integration)

## 📷 Usage

1. Run the script:

```bash
python heart_rate_monitor.py
```

1. Place your **fingertip on the webcam**.
2. Wait ~10 seconds.
3. The BPM will be displayed in the terminal and plotted.


## ⚙️ Customization

- You can modify the **sampling time** and **frame rate** to suit your needs:

```python
sampling_time = 10  # seconds to capture data
fps = 30            # frames per second
```

- Increasing `fps` or `sampling_time` can improve **accuracy** by capturing more data points.


## 📚 Literature References

- Zhang, Z., “Photoplethysmography-Based Heart Rate Monitoring in Physical Activities via Webcam,” *IEEE Transactions on Biomedical Engineering*, 2014.
- Espressif Systems, “ESP32 Technical Reference Manual,” Espressif, 2020.
- Allen, J., “Photoplethysmography and its application in clinical physiological measurement,” *Physiol. Meas.*, 2007.


## 📷 Screenshots
<img width="50" alt="image" src="https://github.com/user-attachments/assets/f4398cb0-dcf3-4be7-a96a-0491a061a92c" />
<img width="660" alt="image" src="https://github.com/user-attachments/assets/1e632fcc-22d9-4e23-91d1-7101c96d5682" />
<img width="376" alt="image" src="https://github.com/user-attachments/assets/1ffeef5b-af1e-4d2a-96a2-ed40eeb3c277" />

