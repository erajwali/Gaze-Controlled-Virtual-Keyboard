Gaze-Controlled Virtual Keyboard System

A web-based virtual keyboard that allows users to type using only eye gaze and blink detection through a standard webcam. This project combines webcam eye tracking, blink-based selection, predictive text, and custom gaze filtering to create a low-cost assistive communication system.

Overview

The goal of this project is to make computer interaction more accessible for users who may not be able to use a traditional keyboard, mouse, or touchscreen. The system tracks where the user is looking on the screen, highlights the closest keyboard button, and uses a blink as a click input. Predictive text suggestions help reduce the number of selections needed to type full words.

This project was developed for Computer Systems Lab 2026.

Features
Webcam-based gaze tracking using WebGazer.js
Blink detection using MediaPipe Face Mesh
Eye Aspect Ratio (EAR)-based blink classification
Virtual keyboard with large gaze-friendly buttons
Predictive text suggestions using the Datamuse API
Gaze smoothing and filtering for more stable cursor control
Calibration system using screen-positioned calibration dots
Recalibration button for correcting gaze drift
Manual mouse-dot mode for testing and debugging
System Architecture

The system follows this general pipeline:

Webcam input is captured in the browser.
WebGazer estimates the user’s gaze position.
Raw gaze data is filtered using median filtering, speed-based outlier rejection, adaptive smoothing, and other stabilization techniques.
MediaPipe Face Mesh detects facial landmarks around the eyes.
Eye Aspect Ratio is calculated to detect intentional blinks.
The gaze cursor highlights the nearest keyboard or suggestion button.
A blink triggers a click on the highlighted target.
The selected key or word suggestion updates the text output box.
Technologies Used
HTML
CSS
JavaScript
WebGazer.js
MediaPipe Face Mesh
Datamuse API
How It Works
Gaze Tracking

The program uses WebGazer.js to estimate the user’s gaze coordinates from webcam input. Because raw webcam gaze data can be noisy, the system applies additional filtering to make cursor movement more stable and usable.

Blink Detection

MediaPipe Face Mesh detects facial landmarks around the eyes. The system calculates Eye Aspect Ratio (EAR), which decreases when the eyes close. During setup, the user keeps their eyes open so the system can calculate a baseline EAR value. A blink is detected when the EAR drops below a percentage of this baseline for multiple frames.

Predictive Text

As the user types, the program extracts the current word prefix and sends it to the Datamuse API. The top suggested words are displayed as large buttons above the keyboard. Selecting a suggestion replaces the current prefix with the full word.

User Interface

The keyboard is designed for gaze interaction. Buttons are larger than a normal keyboard, the text box is kept compact, and the suggestion bar is easy to target. The system highlights the current gaze target so the user can confirm what will be selected before blinking.

Installation
Clone this repository:
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
Open the project folder:
cd YOUR-REPOSITORY
Open the main HTML file in a browser.

Depending on your browser security settings, webcam access may require running the project through a local server instead of opening the HTML file directly.

One simple option is to use Python:

python3 -m http.server 8000

Then open:

http://localhost:8000
Usage
Open the application in a browser.
Allow webcam access when prompted.
Complete the gaze calibration by clicking each calibration dot while looking at it.
Look at a keyboard button or word suggestion.
Blink to select the highlighted target.
Use the recalibration button if the gaze cursor starts drifting.
Controls
Blink: Select the current highlighted key or suggestion.
Recalibrate button: Restart gaze calibration.
Backquote key (`): Toggle manual mouse-dot mode for testing.
M key: Toggle raw/smoothed mode.
L key: Toggle logging.
E key: Export gaze logs.
Project Status

This project is a working proof of concept. It demonstrates that gaze and blink input can be used for hands-free typing with a standard webcam. However, it is not a finished medical or clinical assistive device.

Limitations
Webcam gaze tracking is less accurate than specialized eye-tracking hardware.
Lighting changes can affect gaze and blink detection.
Calibration may drift over time.
Blink detection thresholds may need adjustment for different users.
Predictive text depends on an internet connection because it uses the Datamuse API.
The system has not yet been tested with a large group of users.
Future Improvements
Add quantitative testing for accuracy, speed, and error rate.
Improve gaze calibration and automatic drift correction.
Add local predictive text to remove API dependence.
Add text-to-speech output.
Add customizable keyboard layouts.
Add high-contrast and accessibility display modes.
Support dwell selection as an alternative to blink selection.
Deploy as a hosted web application.
Demo

Project demo video:
https://youtu.be/FqW2EBVEN9Q?si=MVg4WxvfXdoadUJX

Authors

Akhil Saladi
Eraj Wali

Computer Systems Lab
2026

Acknowledgments

This project uses the following open-source or public tools:

WebGazer.js: https://webgazer.cs.brown.edu/
MediaPipe Face Mesh: https://developers.google.com/mediapipe
Datamuse API: https://www.datamuse.com/api/
