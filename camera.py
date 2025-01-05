import threading
import time
import cv2
import os
import subprocess
from ultralytics import YOLO  # Import YOLO from Ultralytics

class Camera:
    def __init__(self, camIndex):
        self.thread = None
        self.current_frame = None
        self.is_running: bool = False
        self.is_recording: bool = False
        self.camera = cv2.VideoCapture(camIndex)
        self.ffmpeg_process = None
        self.yolo_model = YOLO('yolov8m.pt')  # Load the YOLOv8 model

        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.frame_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_rate = int(self.camera.get(cv2.CAP_PROP_FPS)) or 30

    def detect_objects(self, frame):
        """Run object detection on the given frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        resized_frame = cv2.resize(rgb_frame, (640, 640))  # Resize to 640x640
        results = self.yolo_model(resized_frame)  # Inference using YOLOv8
        results = self.yolo_model(resized_frame, conf=0.6)  # Increase confidence threshold
        
        # Save debug frame
        #cv2.imwrite("live_frame_debug.jpg", resized_frame)  # Save the resized frame
         
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence
            cls = int(box.cls[0])  # Class ID
            print(f"Detected {self.yolo_model.names[cls]} with confidence {conf}")
            label = f"{self.yolo_model.names[cls]}: {conf:.2f}"
            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame
    
    def get_frame(self):
        if self.current_frame is not None:
            # Perform detection on the current frame
            detected_frame = self.detect_objects(self.current_frame.copy())
            #cv2.imwrite("debug_frame.jpg", detected_frame)
            return detected_frame
        return None

    def start_recording(self, path):
        if not self.is_recording:
            os.makedirs(path, exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            self.recording_path = os.path.join(path, f"{timestamp}.mp4")

            # Start FFmpeg process
            self.ffmpeg_process = subprocess.Popen(
                [
                    "ffmpeg",
                    "-y",  # Overwrite output file
                    "-loglevel", "error",  # Disable FFmpeg logs
                    "-f", "rawvideo",
                    "-vcodec", "rawvideo",
                    "-pix_fmt", "bgr24",
                    "-s", f"{self.frame_width}x{self.frame_height}",
                    "-r", str(self.frame_rate),
                    "-i", "-",  # Read input from stdin
                    "-c:v", "libx264",
                    "-preset", "ultrafast",
                    "-pix_fmt", "yuv420p",
                    self.recording_path,
                ],
                stdin=subprocess.PIPE
            )

            self.is_recording = True
            print(f"Recording started: {self.recording_path}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.ffmpeg_process:
                self.ffmpeg_process.stdin.close()
                self.ffmpeg_process.wait()
                self.ffmpeg_process = None
            print(f"Recording stopped. File saved: {self.recording_path}")

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
            
#    def get_frame(self):
#        return self.current_frame

    def _capture(self):
        self.is_running = True
        while self.is_running:
            ret, frame = self.camera.read()
            if ret:
                # Perform detection directly
                detected_frame = self.detect_objects(frame.copy())
                self.current_frame = detected_frame
                if self.is_recording and self.ffmpeg_process:
                    try:
                        self.ffmpeg_process.stdin.write(detected_frame.tobytes())
                    except Exception as e:
                        print(f"Error writing frame to FFmpeg: {e}")

