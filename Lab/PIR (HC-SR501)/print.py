import time
import random

print("PIR Sensor initializing... Please wait 30 seconds")
time.sleep(2)  # shortened for demo

print("PIR Sensor ready!")

try:
    while True:
        # Randomly simulate sensor failure
        failure_chance = random.randint(1, 10)

        if failure_chance == 1:
            print("Error: Sensor not detected!")
        
        else:
            # Simulate motion / no motion
            motion = random.choice([0, 1])

            if motion == 1:
                print("Motion Detected!")
            else:
                print("No Motion")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user")