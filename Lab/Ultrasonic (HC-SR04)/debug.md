
STEP 1 — Verify GPIO setup works

import RPi.GPIO as GPIO

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print("GPIO setup successful")

GPIO.cleanup()

Expected: "GPIO setup successful"

If error:
- Library not installed
- Wrong permissions → use sudo

STEP 2 — Check TRIG pin toggling

import RPi.GPIO as GPIO
import time

TRIG = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)

try:
    while True:
        print("Sending trigger pulse")
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # 10µs
        GPIO.output(TRIG, False)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

Verify with multimeter or LED + resistor
Expected: activity every second
If not working: wrong pin number, wiring issue

STEP 3 — Check ECHO pin responsiveness

import RPi.GPIO as GPIO
import time

ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        val = GPIO.input(ECHO)
        print(val)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

Expected:
- Mostly 0 → idle
- Occasional 1 → sensor responding

Always 0 → TRIG not reaching sensor, sensor not powered, wiring wrong
Always 1 → voltage divider missing, GPIO risk

STEP 4 — Check TRIG → ECHO interaction

import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        print("Trigger sent")

        for _ in range(20):
            print(GPIO.input(ECHO), end=" ")
            time.sleep(0.01)
        print("\n---")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

Expected: "Trigger sent" followed by 0 0 1 1 1 0 0 ... (echo pulse)

STEP 5 — Add timing with safety

import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def debug_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            print("Timeout waiting for ECHO HIGH")
            return None
        pulse_start = time.time()

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            print("Timeout waiting for ECHO LOW")
            return None
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    print(f"Pulse duration: {duration:.6f}")
    return duration

try:
    while True:
        debug_distance()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

Interpretation:
- Timeout waiting for ECHO HIGH → TRIG not working or sensor dead
- Timeout waiting for ECHO LOW → ECHO stuck HIGH, voltage issue
- Pulse duration very small → object too close or noise
- Pulse duration very large → no object or wrong reading

STEP 6 — Final distance print

distance = duration * 17150
print(f"Distance: {distance:.2f} cm")

Hardware Debug Checklist:
- Correct pins (BCM vs BOARD)
- Proper GND connection
- Voltage divider present
- Sensor orientation correct
- Jumper wires tight

Most Common Failures:
1. No voltage divider
2. Wrong pin numbering
3. Infinite loop (no timeout)
4. Sensor noise
5. Power instability