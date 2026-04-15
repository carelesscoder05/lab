
First: How the sensor actually works

The HC-SR04 measures distance using time-of-flight:

1. Send a 10µs HIGH pulse to TRIG
2. Sensor emits ultrasonic waves (~40 kHz)
3. Waves reflect from object
4. ECHO pin goes HIGH for the time taken
5. Distance = (Time × 34300) / 2 cm

- 34300 cm/s = speed of sound
- Divide by 2 → signal goes to object + back

Pi Safety

- ECHO pin = 5V output
- Raspberry Pi GPIO = 3.3V max

Voltage divider is required to protect GPIO.

Step 1: Wiring

HC-SR04 → Raspberry Pi

HC-SR04 Pin | Connect to
------------|-------------------
VCC         | 5V (Pin 2)
GND         | GND (Pin 6)
TRIG        | GPIO 23 (Pin 16)
ECHO        | GPIO 24 (Pin 18) via voltage divider

Voltage Divider (ECHO → Pi)

Use 2 resistors:
- R1 = 1kΩ
- R2 = 2kΩ

ECHO ---- R1 ----+---- GPIO24
                 |
                 R2
                 |
                 GND

Step 2: Install Required Library

sudo apt update
sudo apt install python3-rpi.gpio
sudo apt install python3-gpiozero
sudo usermod -a -G gpio $USER

Step 3: Full Python Code (gpiozero version)

from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=24, trigger=23)  # GPIO pins

try:
    while True:
        distance = sensor.distance * 100  # cm
        print(f"Distance: {distance:.2f} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")

Step 3: Full Python Code (RPi.GPIO version)

import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    print("Measuring Distance... Press Ctrl+C to stop")
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped by User")
finally:
    GPIO.cleanup()

Deep Understanding of Code Flow

TRIG Pulse:
- 10µs HIGH pulse triggers sensor

First while loop:
- Wait for ECHO to go HIGH, captures start time

Second while loop:
- Measure duration ECHO is HIGH, round-trip travel time

Why 17150?
- 34300 cm/s ÷ 2 = 17150

Sample Output

Measuring Distance... Press Ctrl+C to stop
Distance: 24.37 cm
Distance: 24.12 cm
Distance: 23.98 cm
Distance: 45.22 cm

Step-by-Step Debugging Strategy

1. Check Power
- Sensor should not heat up
- No response → wiring issue

2. Test TRIG manually

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
print("Trigger sent")

3. Check ECHO pin activity

while True:
    print(GPIO.input(ECHO))
    time.sleep(0.1)

Expected:
- 0 → idle
- 1 → when object detected

If always 0:
- TRIG not working
- Wrong pin mapping

If always 1:
- ECHO shorted
- Voltage divider issue

If stuck in loop:
- Add timeout

timeout = time.time() + 1
while GPIO.input(ECHO) == 0:
    if time.time() > timeout:
        return None

Key Takeaways

- HC-SR04: time measurement → distance conversion
- GPIO used for output (TRIG) and input (ECHO)
- Timing precision is critical
- Voltage mismatch is the main failure point