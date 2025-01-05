# Video-Streaming-Solution
Video Streaming Solution + AI Inference using Python, OpenCV, FFMPEG &amp; YOLOV8. It fetches camera stream from WebCam or IP camera and stream it on Browser over HTTP. Apart from Live Streaming it also has features of video recording and playback. 

## Overview
This is to demonstrate a way to broadcast video from a webcam to web clients (browsers) using:

- Python
- OpenCV (opencv-python) - getting frames from camera and apply object detection
- WebSocket
- Http server
- FFmpeg - To record stream locally in mp4 format

## Concepts Covered in the source codes
- Using OpenCV (*cv2*) to read frames from the webcam
- Using OpenCV to process the frames
- Using WebSocket to push the frames to connected clients (browsers)
- Asynchronous tasks using *asyncio*
- Multi-threading using *threading*

## Getting started
Environment Setup : 
a) Install packages like ffmpeg.
b) Install Anaconda to create Virtual Environment so that it does not affect the main system environment.
   Link : 
	https://docs.anaconda.com/anaconda/install/#manual-shell-init-linux

   Follow the installation instructions mentioned in the link to install and configure anaconda.
   I have considered Linux (Ubuntu 22.04) as my host environment. You can install version as per your Host OS.

   Steps to Create & Configure Virtual Environment :
   
   Open a Terminal & Enter below commands -
   1) source ~/anaconda3/bin/activate (This path may vary based on the installation path selected for anaconda)
   2) conda create --name <name_of_env> python=3.11 (It will ask to install some package, select y)
   3) conda activate <name_of_env>
   4) mkdir -p ~/projects && cd ~/projects
   5) git clone https://github.com/avp24/Video-Streaming-Solution.git
   6) cd video_streaming_solution
   7) pip install -r requirements.txt
   8) pip install ultralytics (This command will take some time as it will be installing all the packages w.r.t yolov8 for Class Detections 
      on Camera Stream)
   9) pip install websockets

**Note :** Environment Creation steps have to be executed once. 
After Virtual Environment configuration whenever a new terminal is opened enter commands -

--> source ~/anaconda3/bin/activate

--> conda activate <name_of_env> (Can use conda env list to check if multiple environments are created) 

Execute Application :
1) cd ~/projects/video_streaming_solution
2) python main.py
It will start the script and http server will start on port 8088
3) Open browser and navigate to <ip_address>:8088 or 127.0.0.1:8088.
You should be able to see Live Stream with Object Detection enabled. This works for multiple clients.  Hence, you may open multiple browser windows/tabs to test.

## Disclaimer
For This Video Streaming Solution have used Ubuntu 22.04 as Host OS & used Webcam for verification.

**Note :** 

a) It is recommended to check this solution on GPU enabled system as we are using Yolo based AI inference for object detection
which requires GPU for better performance.

b) This solution can be used with IP camera as well. To use IP camera stream (RTSP or HTTP),
In main.py replace camera = Camera(0) with camera = Camera("rtsp://<username>:<password>@<ip-address>:<port>/<path>").

Ex : IP camera with RTSP URL - camera = Camera("rtsp://admin:password@192.168.1.10:554/stream")

IP camera with HTTP URL - camera = Camera("http://192.168.1.10:8080/video")

Before Directly using IP camera with application verify IP camera stream is accessible on video player like VLC using the URL.
 
