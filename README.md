# Driver Drowsiness Detection System

This project is a real-time **Driver Drowsiness Detection System** that monitors the user's eyes using a webcam. It uses **MediaPipe Face Mesh** to track facial landmarks and calculates the **Eye Aspect Ratio (EAR)** to detect if eyes are closed for a prolonged time, which could indicate drowsiness. It also features a **GUI with Tkinter** and plays an alert sound if drowsiness is detected.

# Features

- Real-time face and eye detection using **MediaPipe**
- Eye aspect ratio (EAR)–based drowsiness detection logic
- Plays alarm when eyes stay closed beyond threshold
- Logs drowsiness events with timestamp to a text file
- Interactive **Tkinter GUI**
- Live webcam feed embedded in GUI
- Drowsiness count display on screen

# Technologies Used

- Python 3.13
- OpenCV
- MediaPipe
- Pygame (for sound alerts)
- Tkinter (GUI)
- PIL (Image handling in GUI)

# Installation

1. Clone the repository:
   
   git clone https://github.com/your-username/drowsiness-detector.git
   
   cd drowsiness-detector

3. Install the dependencies:
   pip install -r requirements.txt

4. Add an alarm.wav file to the project folder.

# How to Run
python drowsiness_detector.py
Click "Start Detection" to begin.

The system will use your webcam to track eye movements.

Click "Stop" to stop detection and close the webcam.

# How It Works

Captures real-time webcam feed.

Detects facial landmarks using MediaPipe Face Mesh.

Calculates Eye Aspect Ratio (EAR) for both eyes.

If eyes stay closed for more than 3 seconds, it:

Plays an alarm

Logs the event with date/time

Increments the drowsy count on the GUI

# Output

Real-time visual alert: "DROWSINESS ALERT!"
Alarm sound

A file named drowsiness_log.txt containing:

[2025-07-25 14:05:32] Drowsiness Detected

# Log File Example

[2025-07-25 14:01:02] Drowsiness Detected

[2025-07-25 14:03:45] Drowsiness Detected

# Contributing

Pull requests are welcome. Feel free to open issues or submit pull requests.

# Acknowledgments

MediaPipe by Google
OpenCV
Python’s Tkinter and Pygame libraries
