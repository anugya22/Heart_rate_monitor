from flask import Flask, render_template, jsonify, request, session, url_for, send_from_directory
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/measure")
def measure():
    return render_template("measure.html")

@app.route("/theory")
def theory():
    return render_template("theory.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/ads.txt")
def ads():
    return send_from_directory(directory='static', path='ads.txt', mimetype='text/plain')

@app.route("/start", methods=["POST"])
def start_detection():
    data = request.get_json()
    intensity_values = data.get("intensity_values", [])
    sampling_time = data.get("duration", 10)

    if not intensity_values or len(intensity_values) < 10:
        return jsonify({"error": "No or insufficient intensity data received"}), 400

    if max(intensity_values) - min(intensity_values) < 15:
        session["bpm"] = "Unreliable"
        session["smoothed"] = []
        session["peaks"] = []
        return jsonify({"redirect": url_for("result")})

    fps = len(intensity_values) / sampling_time

    # Butterworth bandpass filter
    def butter_bandpass_filter(data, lowcut=0.8, highcut=3.0, fs=30.0, order=3):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = filtfilt(b, a, data)
        return y

    filtered = butter_bandpass_filter(np.array(intensity_values), fs=fps)

    try:
        peaks, _ = find_peaks(filtered, distance=fps / 2.5, height=np.mean(filtered) * 0.9)
    except Exception:
        peaks = []

    if len(peaks) < 2:
        bpm = "Unreliable"
    else:
        bpm_calc = (len(peaks) / sampling_time) * 60
        bpm = round(bpm_calc, 2) if 40 <= bpm_calc <= 200 else "Unreliable"

    session["bpm"] = bpm
    session["smoothed"] = filtered.tolist()
    session["peaks"] = peaks.tolist()

    return jsonify({"redirect": url_for("result")})

@app.route("/result")
def result():
    bpm = session.get("bpm", "Unreliable")
    smoothed = session.get("smoothed", [])
    peaks = session.get("peaks", [])
    return render_template("result.html", bpm=bpm, smoothed=smoothed, peaks=peaks)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
