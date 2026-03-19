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