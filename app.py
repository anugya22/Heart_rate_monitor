from flask import Flask, render_template, jsonify, request, session, url_for
import cv2
import numpy as np
from scipy.signal import find_peaks

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session storage

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/measure")
def measure():
    return render_template("measure.html")

@app.route("/theory")
def theory():
    return render_template("theory.html")

@app.route("/start", methods=["POST"])
def start_detection():
    data = request.get_json()
    intensity_values = data.get("intensity_values", [])
    sampling_time = data.get("duration", 7)

    if not intensity_values:
        return jsonify({"error": "No intensity data received"}), 400

    smoothed = np.convolve(intensity_values, np.ones(5)/5, mode='valid')
    fps = len(intensity_values) / sampling_time
    peaks, _ = find_peaks(smoothed, distance=fps/3, height=np.mean(smoothed) * 0.9)
    bpm = (len(peaks) / sampling_time) * 60

    session["bpm"] = round(bpm, 2)
    session["smoothed"] = smoothed.tolist()
    session["peaks"] = peaks.tolist()

    return jsonify({"redirect": url_for("result")})

@app.route("/result")
def result():
    bpm = session.get("bpm", 0)
    smoothed = session.get("smoothed", [])
    peaks = session.get("peaks", [])
    return render_template("result.html", bpm=bpm, smoothed=smoothed, peaks=peaks)

if __name__ == "__main__":
    app.run(debug=True)
 port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
