// Light/Dark Mode
// Light/Dark Mode Toggle
const toggleBtn = document.getElementById('themeToggle');
toggleBtn?.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');

  // Optional: change the button icon too
  toggleBtn.textContent = document.body.classList.contains('dark-mode') ? "🌞" : "🌓";
});

// Video Preview
const video = document.getElementById('video');
if (video) {
  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
  }).catch(err => {
    console.error("Webcam error: ", err);
  });
}

// Start Measurement
const startBtn = document.getElementById('startBtn');
const result = document.getElementById('result');

if (startBtn) {
  startBtn.addEventListener('click', async () => {
    result.innerText = "Measuring... Please wait 7 seconds.";
    const res = await fetch('/start');
    const data = await res.json();
    result.innerText = `Your BPM: ${data.bpm}`;
  });
}
