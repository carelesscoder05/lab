from gpiozero import MotionSensor
from signal import pause

# PIR connected to GPIO17
pir = MotionSensor(17)

print("PIR Sensor initializing... Please wait 30 seconds")

# gpiozero handles stabilization internally, but we wait for clarity
pir.wait_for_no_motion()

print("PIR Sensor ready!")

# Define actions
def motion_detected():
    print("Motion Detected!")

def motion_stopped():
    print("No Motion")

# Attach event handlers
pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

# Keep program running
pause()




# import RPi.GPIO as GPIO
# import time

# # Use BCM numbering
# GPIO.setmode(GPIO.BCM)

# # PIR sensor connected to GPIO17
# PIR_PIN = 17

# # Set PIR pin as input
# GPIO.setup(PIR_PIN, GPIO.IN)

# print("PIR Sensor initializing... Please wait 30 seconds")

# # Warm-up time
# time.sleep(30)

# print("PIR Sensor ready!")

# try:
#     while True:
#         if GPIO.input(PIR_PIN):
#             print("Motion Detected!")
#         else:
#             print("No Motion")
        
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("\nProgram stopped by user")

# finally:
#     GPIO.cleanup()