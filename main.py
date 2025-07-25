import cv2
import mediapipe as mp
import pygame
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")  # alarm.wav must be in the same directory

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye aspect ratio calculation
def eye_aspect_ratio(landmarks, eye_indices):
    left = landmarks[eye_indices[0]]
    right = landmarks[eye_indices[3]]
    top = landmarks[eye_indices[1]]
    bottom = landmarks[eye_indices[5]]

    width = ((left.x - right.x) ** 2 + (left.y - right.y) ** 2) ** 0.5
    height = ((top.y - bottom.y) ** 2 + (top.x - bottom.x) ** 2) ** 0.5

    return height / width if width != 0 else 0

# Log drowsy event to file
def log_drowsiness():
    with open("drowsiness_log.txt", "a") as file:
        now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file.write(f"{now} Drowsiness Detected\n")

# Main application class with GUI
class DrowsinessApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Driver Drowsiness Detection")
        self.cap = None
        self.canvas = tk.Label(window)
        self.canvas.pack()

        self.start_button = tk.Button(window, text="Start Detection", command=self.start_detection)
        self.start_button.pack()

        self.stop_button = tk.Button(window, text="Stop", command=self.stop_detection)
        self.stop_button.pack()

        self.status_label = tk.Label(window, text="Drowsy Count: 0", font=("Arial", 12))
        self.status_label.pack()

        self.running = False
        self.eye_closed_start_time = None
        self.drowsy_count = 0
        self.drowsy_triggered = False

    def start_detection(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.detect()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.music.stop()

    def detect(self):
        success, frame = self.cap.read()
        if not success:
            return

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)
        current_time = time.time()

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Eye landmarks
                right_eye = [33, 160, 158, 133, 153, 144]
                left_eye = [362, 385, 387, 263, 373, 380]

                right_ratio = eye_aspect_ratio(face_landmarks.landmark, right_eye)
                left_ratio = eye_aspect_ratio(face_landmarks.landmark, left_eye)

                if right_ratio < 0.2 and left_ratio < 0.2:
                    if self.eye_closed_start_time is None:
                        self.eye_closed_start_time = current_time
                        self.drowsy_triggered = False
                    elif (current_time - self.eye_closed_start_time >= 3) and not self.drowsy_triggered:
                        # Drowsiness event
                        cv2.putText(frame, "DROWSINESS ALERT!", (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.play()
                        log_drowsiness()
                        self.drowsy_count += 1
                        self.status_label.config(text=f"Drowsy Count: {self.drowsy_count}")
                        self.drowsy_triggered = True
                else:
                    self.eye_closed_start_time = None
                    self.drowsy_triggered = False
                    pygame.mixer.music.stop()

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.configure(image=imgtk)

        if self.running:
            self.window.after(10, self.detect)

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = DrowsinessApp(root)
    root.mainloop()
