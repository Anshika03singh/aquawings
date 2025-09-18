import cv2
import time
import numpy as np
from dronekit import connect, VehicleMode, LocationGlobalRelative
from inference_sdk import InferenceHTTPClient

# Connect to Pixhawk via MAVLink
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

# Initialize AI detection
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="mV2CN1mPIxjjDgtKWyGs"
)
MODEL_ID = "aqua-wings/2"

# Open camera
cap = cv2.VideoCapture(0)

def arm_and_takeoff(target_altitude):
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialize...")
        time.sleep(1)
    
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print("Arming motors...")
        time.sleep(1)
    
    print("Taking off...")
    vehicle.simple_takeoff(target_altitude)
    
    while True:
        print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def navigate_to(lat, lon):
    target_location = LocationGlobalRelative(lat, lon, 10)
    vehicle.simple_goto(target_location)
    print(f"Navigating to: {lat}, {lon}")

def detect_drowning():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        cv2.imwrite("frame.jpg", frame)
        result = CLIENT.infer("frame.jpg", model_id=MODEL_ID)
        
        for prediction in result["predictions"]:
            if prediction['class'] == "drowning_person":
                print("Drowning person detected!")
                lat, lon = prediction["latitude"], prediction["longitude"]
                navigate_to(lat, lon)
                return
        
        cv2.imshow("Drone View", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()

# Main execution
arm_and_takeoff(10)
detect_drowning()

print("Mission complete. Returning to launch.")
vehicle.mode = VehicleMode("RTL")
vehicle.close()
