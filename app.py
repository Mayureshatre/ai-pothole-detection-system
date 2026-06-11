import cv2
from ultralytics import YOLO
import time
# import tkinter as tk             # <--- GUI COMMENTED OUT
# from tkinter import filedialog   # <--- GUI COMMENTED OUT
# from PIL import Image, ImageTk   # <--- GUI COMMENTED OUT
# import threading                 # <--- GUI COMMENTED OUT

class PotholeDetectionHeadless:
    def __init__(self):
        # --- GUI WINDOW SETUP COMMENTED OUT ---
        # self.root = root
        # self.root.title("AI Pothole Detection System")
        # self.root.geometry("1000x750")
        # ... (Labels and Buttons removed) ...
        # --------------------------------------

        # --- 1. Load Your Custom Model ---
        print("Loading AI Model... please wait.")
        try:
            self.model = YOLO("best.pt") 
            print("✅ Model Loaded Successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Make sure 'best.pt' is in the folder.")
            exit()

        self.cap = None
        self.running = False

    def start_detection(self):
        
        # OPTION 1: Use Live Camera (Default)
        # Change 0 to 1 if using an external USB camera
        video_source = "potholes.mp4" 
        
        # OPTION 2: Use a Video File
        # Uncomment the line below and add your file path
        # video_source = "road_test_video.mp4"

        # ==========================================================
        
        print(f"🚀 Starting Detection on source: {video_source}")
        self.cap = cv2.VideoCapture(video_source)
        self.running = True
        
        # Start the loop directly (no Threading needed without GUI)
        self.process_video()

    def process_video(self):
        """
        Main Loop: Reads frame -> Predicts -> Prints Result
        """
        frame_count = 0
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("End of video or camera error.")
                break

            # Resize to save speed on Raspberry Pi
            frame = cv2.resize(frame, (640, 480))

            # --- AI INFERENCE ---
            # conf=0.45 is the sensitivity
            results = self.model(frame, conf=0.45, verbose=False) 
            
            # Count potholes
            pothole_count = len(results[0].boxes)

            # --- GUI DISPLAY COMMENTED OUT ---
            # annotated_frame = results[0].plot()
            # img = Image.fromarray(...)
            # self.video_label.configure(image=img)
            # ---------------------------------

            # --- NEW: Print Status to Terminal ---
            # We print every 30 frames so the terminal doesn't go crazy
            frame_count += 1
            if frame_count % 10 == 0: 
                if pothole_count > 0:
                    print(f"⚠️ POTHOLE DETECTED! Count: {pothole_count}")
                    # [OPTIONAL] Add Buzzer code here for Pi
                    # GPIO.output(BUZZER_PIN, GPIO.HIGH)
                else:
                    print(f"Status: Clear | Frame {frame_count}", end='\r')

            # Small sleep to prevent CPU overheating
            time.sleep(0.01)

        self.cap.release()
        print("\nStopped.")

if __name__ == "__main__":
    # root = tk.Tk()                # <--- GUI COMMENTED OUT
    app = PotholeDetectionHeadless()
    app.start_detection()           # Starts immediately
    # root.mainloop()               # <--- GUI COMMENTED OUT