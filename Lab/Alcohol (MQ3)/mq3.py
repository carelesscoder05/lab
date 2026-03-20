from gpiozero import DigitalInputDevice
from time import sleep

# MQ-3 D0 connected to GPIO17
sensor = DigitalInputDevice(17)

print("Alcohol Sensor Initialized...")
print("Waiting for readings...\n")

while True:
    if sensor.value == 1:
        print("Alcohol Detected!")
    else:
        print("No Alcohol Detected")
    
    sleep(1)














# import RPi.GPIO as GPIO
# import time

# # GPIO setup
# GPIO.setmode(GPIO.BCM)
# MQ3_DO = 18      # GPIO17 (Pin 11)

# GPIO.setup(MQ3_DO, GPIO.IN)

# print("MQ-3 Alcohol Sensor (Digital Output)")
# print("Warming up sensor... Please wait (20 seconds)")
# time.sleep(20)

# while True:
#     sensor_state = GPIO.input(MQ3_DO)

#     if sensor_state == GPIO.LOW:
#         print("️ Alcohol Detected!")
#     else:
#         print("No alcohol detected")

#     time.sleep(1)
