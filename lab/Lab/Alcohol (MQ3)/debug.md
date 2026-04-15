
Since you’re using D0 (digital mode), debugging is mostly about:

- Wiring
- GPIO reading
- Sensor threshold (potentiometer)

STEP-BY-STEP DEBUGGING APPROACH

Follow this in order. Don’t skip steps.

STEP 1: Check Basic GPIO Reading

First verify that the Raspberry Pi can read the pin at all.

from gpiozero import Button
from time import sleep

sensor = Button(17)

while True:
    print(sensor.is_pressed)
    sleep(1)

Expected Output

- True → HIGH (Alcohol detected)
- False → LOW (No alcohol)

If this changes → GPIO + wiring is OK  
If stuck → go to next step

STEP 2: Check Sensor LED (Hardware Debug) --> if led present

Look at the MQ-3 module:

- Power LED → should be ON always
- Detection LED → changes when alcohol is present

Interpretation

LED Behavior            Meaning
No LED at all           Power issue
Only power LED ON       Threshold too high
Detection LED always ON Threshold too low

STEP 3: Adjust Potentiometer (MOST COMMON FIX)

Use a screwdriver:

1. Run the debug code
2. Slowly turn the potentiometer
3. Observe:
   - LED change
   - Terminal output change

Goal

No alcohol → False  
Alcohol → True

STEP 4: Verify Wiring

Double-check connections:

MQ-3 | Raspberry Pi
VCC  | 5V
GND  | GND
D0   | GPIO17

Common Mistakes

- Using 3.3V instead of 5V
- No common GND
- Wrong GPIO pin

STEP 5: Force Test the GPIO Pin

This isolates whether the problem is:
Sensor OR Raspberry Pi

Test:

Disconnect D0 wire and:

- Touch GPIO17 to 3.3V → should print True
- Touch GPIO17 to GND → should print False

Result

Result       Problem
Works        Sensor issue
Doesn’t work GPIO/config issue

STEP 6: Final Debug Code (Clear Output)

Use this to clearly see state changes:

from gpiozero import DigitalInputDevice
from time import sleep

sensor = DigitalInputDevice(17)

prev = None

while True:
    current = sensor.value
    
    if current != prev:
        if current:
            print("DEBUG: HIGH → Alcohol Detected")
        else:
            print("DEBUG: LOW → No Alcohol")
    
    prev = current
    sleep(0.2)

Why this is useful

- Prints only when state changes
- Helps detect:
  - Flickering signals
  - Noise
  - Improper threshold

FINAL QUICK CHECKLIST (Exam Ready)

If not working, say:

1. “I verified GPIO input using a test script”
2. “I checked sensor LED status”
3. “I calibrated threshold using potentiometer”
4. “I validated wiring connections”
5. “I isolated GPIO using manual HIGH/LOW test”
