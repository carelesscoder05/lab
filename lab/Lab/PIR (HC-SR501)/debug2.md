Systematic debugging approach for PIR sensor using RPi.GPIO. Focus on layer-by-layer verification: GPIO → pin signal → sensor behavior.

STEP 1 — Verify GPIO Library Works

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
print("GPIO setup successful")
GPIO.cleanup()

Expected output:
GPIO setup successful

If fails:
- Run with sudo
- Ensure library installed

STEP 2 — Check Pin Configuration

import RPi.GPIO as GPIO

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("Reading GPIO pin...")

for i in range(10):
    val = GPIO.input(PIR_PIN)
    print(f"Read value: {val}")

GPIO.cleanup()

Interpretation:
Output      → Meaning
Always 0    → No signal / wiring issue
Always 1    → Stuck HIGH / sensor issue
Changing    → Good sign

STEP 3 — Check Raw Signal Stability

import RPi.GPIO as GPIO
import time

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("Monitoring raw signal (no logic)...")

try:
    while True:
        print(GPIO.input(PIR_PIN))
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

Observation:
- Rapid flickering → noise / unstable power
- Always 0 → no detection / wrong wiring
- Always 1 → sensor stuck / too sensitive

STEP 4 — Verify PIR Output Behavior

import RPi.GPIO as GPIO
import time

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("Waiting for PIR to stabilize...")
time.sleep(30)

print("Start moving in front of sensor...")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("HIGH → Motion detected")
        else:
            print("LOW → No motion")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

STEP 5 — Check Wiring (Critical Step)

Correct Wiring:
- VCC → 5V (Pin 2)
- GND → GND (Pin 6)
- OUT → GPIO17 (Pin 11)

Common Mistakes:
- OUT connected to wrong pin
- VCC/GND swapped
- Loose jumper wires

STEP 6 — Power & Warm-Up Check

- PIR needs 30–60 seconds to stabilize
- Output may be random during this period

Fix:
time.sleep(30)

STEP 7 — Check Sensor Hardware

- Observe LEDs:
    - Power LED ON → good
- Adjust knobs:
    - Sensitivity
    - Delay time

STEP 8 — Try Internal Pull-down (Advanced Debug)

GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

STEP 9 — Rule Out GPIO Damage

- Disconnect PIR
- Touch GPIO pin to 3.3V
print(GPIO.input(PIR_PIN))

If:
- Changes → GPIO works
- No change → pin issue

Debugging Flow (Mental Model):

1. Software Layer → GPIO initializes?
2. GPIO Layer → Can read HIGH/LOW?
3. Signal Layer → Does pin change?
4. Sensor Layer → PIR responds to motion?
5. Hardware Layer → Wiring, power, stability

Final Insight:

Most PIR issues stem from:
- Improper warm-up
- Loose wiring
- Expecting instant response
- Not accounting for PIR delay behavior