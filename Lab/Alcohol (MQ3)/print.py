import time
import random

print("Starting Alcohol Sensor Simulation...\n")

while True:
    # Randomly simulate detection
    # 70% chance to detect alcohol, 30% chance no detection
    detected = random.choices([True, False], weights=[7, 3])[0]

    if detected:
        print("Alcohol Detected!")
    else:
        print("No Alcohol Detected")

    print("-----------------------------")
    time.sleep(1)  # 1-second interval