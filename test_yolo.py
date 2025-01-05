from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')  # Replace with your model
frame = cv2.imread('test.jpg')  # Replace with a test image
results = model(frame)

# Draw detections on the frame
for box in results[0].boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
    conf = box.conf[0]  # Confidence
    cls = int(box.cls[0])  # Class ID
    label = f"{model.names[cls]}: {conf:.2f}"
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow("Detections", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

