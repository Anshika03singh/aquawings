import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="mV2CN1mPIxjjDgtKWyGs"
)

MODEL_ID = "aqua-wings/2"

# Open the webcam
cap = cv2.VideoCapture("output_video.mp4")

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
 
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    image_path = "temp_frame.jpg"
    cv2.imwrite(image_path, frame)

    result = CLIENT.infer(image_path, model_id=MODEL_ID)

    for prediction in result["predictions"]:
        x, y, w, h = int(prediction["x"]), int(prediction["y"]), int(prediction["width"]), int(prediction["height"])
        label = f"{prediction['class']} ({prediction['confidence']:.2f})"
        
        cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
        
        cv2.putText(frame, label, (x - w // 2, y - h // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("Aqua Wings Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()