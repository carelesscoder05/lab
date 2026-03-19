
1. Hardware Connections

PIR Pin → Raspberry Pi Pin
VCC     → 5V (Pin 2)
GND     → GND (Pin 6)
OUT     → GPIO17 (Pin 11)

2. Install Required Library

sudo apt update
sudo apt install python3-rpi.gpio
sudo apt install python3-gpiozero
sudo usermod -a -G gpio $USER

3. Complete Code (gpiozero Version)

from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(17)

print("PIR Sensor initializing... Please wait 30 seconds")
pir.wait_for_no_motion()
print("PIR Sensor ready!")

def motion_detected():
    print("Motion Detected!")

def motion_stopped():
    print("No Motion")

pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

pause()

4. Conceptual Differences from RPi.GPIO

1. Object Abstraction

pir = MotionSensor(17)

- Models sensor as an object with behavior instead of manual pin reads

2. Event-Driven Model

Callbacks replace polling:

pir.when_motion = motion_detected

- gpiozero monitors pin continuously
- Calls function only on state changes

3. Blocking with pause()

pause()

- Keeps program alive
- No busy looping

4. Built-in Stabilization

pir.wait_for_no_motion()

- Ensures sensor settles before starting
- Equivalent to manual warm-up

5. Internal Working

MotionSensor treats PIR as digital input device, applying:

- Debouncing
- State change detection
- Optional threshold timing

6. Expected Output

PIR Sensor initializing... Please wait 30 seconds
PIR Sensor ready!
No Motion
Motion Detected!
No Motion
Motion Detected!

7. Key Advantage Summary

Feature          | RPi.GPIO | gpiozero
---------------- | -------- | --------
Setup complexity | Manual   | Minimal
Loop required    | Yes      | No
Event handling   | Manual   | Built-in
Readability      | Medium   | High

8. Optional Advanced Tuning

Sensitivity:

pir = MotionSensor(17, threshold=0.5)

Timing:

pir = MotionSensor(17, queue_len=1, sample_rate=10)

- Useful to filter noise
- Provides precise motion detection timing