Good — now let’s build a proper LCD-only debugging workflow (no DHT11, no extra complexity). The goal is to isolate issues layer by layer and not guess.

Step-by-Step Debug Approach (LCD + Raspberry Pi)

Step 1: Power & Contrast Check (No Code)

Before writing any code:

1. Power ON Raspberry Pi

2. Check LCD:

- Backlight ON → power is fine
- Backlight OFF → check VDD (5V), GND, A/K pins

3. Adjust potentiometer:

- You should see black blocks on first row

Interpretation:

Observation         Meaning
No light            Power issue
Light but no blocks Contrast (VO) issue
Blocks visible      LCD is powered and working

This step alone eliminates ~50% of issues

Step 2: Minimal LCD Test (RPLCD)

Run this simple test:

from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

print("[DEBUG] Starting LCD test...")

GPIO.setmode(GPIO.BCM)

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16, rows=2,
    pin_rs=26,
    pin_rw=None,
    pin_e=19,
    pins_data=[13, 6, 5, 11]
)

try:
    print("[DEBUG] LCD initialized")

    lcd.clear()
    print("[DEBUG] Cleared LCD")

    lcd.write_string("TEST")
    print("[DEBUG] Wrote TEST")

    time.sleep(5)

except Exception as e:
    print("[ERROR]", e)

finally:
    lcd.clear()
    GPIO.cleanup()
    print("[DEBUG] Cleanup done")

Step 3: Interpret Output

Case 1: Console prints, LCD blank

Problem = contrast or wiring

Case 2: LCD shows random characters

Problem = wrong data pin order

Fix:

pins_data=[13, 6, 5, 11]  (Must match D4–D7 exactly)

Case 3: LCD shows only black boxes

Problem = LCD not initialized properly

- Check RS, E pins
- Check RW is grounded

Case 4: Program crashes

Problem = library / GPIO setup

Step 4: Pin-Level Debug (Very Important)

Test if GPIO pins are actually toggling:

import RPi.GPIO as GPIO
import time

pins = [26, 19, 13, 6, 5, 11]

GPIO.setmode(GPIO.BCM)

for p in pins:
    GPIO.setup(p, GPIO.OUT)

print("[DEBUG] Toggling pins...")

try:
    while True:
        for p in pins:
            GPIO.output(p, 1)
        time.sleep(1)

        for p in pins:
            GPIO.output(p, 0)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

What to check:

- Use LED or multimeter
- Pins should go HIGH/LOW

If not → GPIO issue, not LCD

Step 5: Manual LCD Control (Bypass RPLCD)

If still not working, test hardware directly:

import RPi.GPIO as GPIO
import time

RS, E = 26, 19
D4, D5, D6, D7 = 13, 6, 5, 11

GPIO.setmode(GPIO.BCM)

for pin in [RS, E, D4, D5, D6, D7]:
    GPIO.setup(pin, GPIO.OUT)

def pulse():
    GPIO.output(E, 1)
    time.sleep(0.001)
    GPIO.output(E, 0)

def send4(bits):
    GPIO.output(D4, bits & 1)
    GPIO.output(D5, (bits >> 1) & 1)
    GPIO.output(D6, (bits >> 2) & 1)
    GPIO.output(D7, (bits >> 3) & 1)
    pulse()

def send(byte, mode):
    GPIO.output(RS, mode)
    send4(byte >> 4)
    send4(byte & 0x0F)
    time.sleep(0.002)

def init():
    send(0x33, 0)
    send(0x32, 0)
    send(0x28, 0)
    send(0x0C, 0)
    send(0x06, 0)
    send(0x01, 0)

def write(msg):
    for c in msg:
        send(ord(c), 1)

try:
    print("[DEBUG] Initializing LCD manually...")
    init()
    write("HELLO")
    print("[DEBUG] Message sent")

    time.sleep(5)

finally:
    GPIO.cleanup()

Interpretation:

Result     Conclusion
Works here RPLCD issue
Fails here Hardware issue

Step 6: Final Isolation Logic

Follow this exact order:

Power → Contrast → RPLCD test → GPIO test → Manual LCD control

Quick Debug Checklist (Exam Style)

- Backlight ON?
- Contrast adjusted?
- RW connected to GND?
- Correct GPIO mode (BCM)?
- Data pins in correct order?
- RS and E connected properly?

Key Insight

Most LCD failures are not software problems.

They are:

- Contrast (VO) issue
- Wiring mistake
- Wrong pin mapping