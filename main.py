import tkinter as tk                            #tool for making windows, buttons,and text
from tkinter import filedialog, Label, Button  #tool to open the "Select File" pop-up window.
import cv2
from PIL import Image, ImageTk                  #works as a translator between cv2(BGR) and tkinter(RGB)
from ultralytics import YOLO
import threading
import time

class PotholeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pothole Detection System (YOLOv8) - Smart Filter")
        self.root.geometry("1000x750")
        self.root.configure(bg="#2c3e50")

        print("Loading AI Model... please wait.")
        try:
            self.model = YOLO("best.pt") 
            print("✅ Model Loaded Successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Make sure 'best.pt' is in the folder.")

        self.cap = None             #will hold video file or live camera
        self.running = False       #type of switch to stop and start
        self.latest_imgtk = None  # will store the next frame for GUI

        self.title_label = Label(root, text="Pothole Detection System", 
                               bg="#2c3e50", fg="white", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        self.video_label = Label(root, bg="black")          # Video Display Area
        self.video_label.pack(pady=10)

        self.btn_frame = tk.Frame(root, bg="#2c3e50")        # Control Buttons
        self.btn_frame.pack(pady=20)

        self.btn_select = Button(self.btn_frame, text="📁 Select Video", command=self.select_video, 
                               font=("Arial", 14), bg="#3498db", fg="white", width=15)
        self.btn_select.grid(row=0, column=0, padx=10)

        self.btn_camera = Button(self.btn_frame, text="📹 Live Camera", command=self.start_camera, 
                               font=("Arial", 14), bg="#e67e22", fg="white", width=15)
        self.btn_camera.grid(row=0, column=1, padx=10)

        self.btn_stop = Button(self.btn_frame, text="🛑 Stop", command=self.stop_detection, 
                             font=("Arial", 14), bg="#c0392b", fg="white", width=15)
        self.btn_stop.grid(row=0, column=2, padx=10)

        # Stats Label
        self.stats_label = Label(root, text="Status: Ready", bg="#2c3e50", fg="#f1c40f", font=("Arial", 14))
        self.stats_label.pack(pady=10)

        self.update_gui_loop()              # Start the GUI Update Loop

    def update_gui_loop(self):
        if self.latest_imgtk:                   # prevents flickering 
            self.video_label.imgtk = self.latest_imgtk
            self.video_label.configure(image=self.latest_imgtk)
        self.root.after(30, self.update_gui_loop)           #Checks for a new image every 30ms

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if path:
            self.stop_detection()
            self.cap = cv2.VideoCapture(path)
            self.running = True
            threading.Thread(target=self.process_video, daemon=True).start()

    def start_camera(self):
        self.stop_detection()
        self.cap = cv2.VideoCapture(0)
        self.running = True
        threading.Thread(target=self.process_video, daemon=True).start()

    def stop_detection(self):
        self.running = False
        time.sleep(0.1)
        if self.cap:
            self.cap.release()
        self.video_label.configure(image='')
        self.stats_label.config(text="Status: Stopped")

    def process_video(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480)) # Resize. to increase speed

            results = self.model(frame, conf=0.45, verbose=False)   # Run the model, but turn off the default drawing (verbose=False)
            
            pothole_count = 0

            for box in results[0].boxes:

                x1, y1, x2, y2 = box.xyxy[0].tolist()       #coordinate of box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                w = x2 - x1     #height and width of detected object
                h = y2 - y1

                aspect_ratio = h / w

                if aspect_ratio > 1.2:         # If Ratio > 1.2, it means it can be human or a pole
                    continue
                
                pothole_count += 1             #otherwise, pothole 

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) #red box for pothole
                
                # Draw Label Background
                label = f"Pothole {box.conf[0]:.2f}"
                (w_text, h_text), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - 20), (x1 + w_text, y1), (0, 0, 255), -1)
                
                # Draw Text
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                          0.5, (255, 255, 255), 1)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #covesion to RGB
            img = Image.fromarray(rgb_image)                     #then to PIL format
            imgtk = ImageTk.PhotoImage(image=img)                #then to tkinter format
            self.latest_imgtk = imgtk                             #transfer to GUI

            # Update text status
            self.root.after(0, lambda: self.stats_label.config(
                text=f"Status: Running | Potholes Detected: {pothole_count}"
            ))
            
            time.sleep(0.01)

        self.running = False

if __name__ == "__main__":
    root = tk.Tk()                  #create the main window
    app = PotholeDetectionApp(root) #loads th logic 
    root.mainloop()                 #keeps thw window open and wait for clicks