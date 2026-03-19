
1. Hardware Connections (R305 ↔ Raspberry Pi)

The R305 uses UART (TTL serial).

R305 Pin | Raspberry Pi Pin
VCC      | 5V (Pin 2 or 4)
GND      | GND (Pin 6)
TX       | RX (GPIO15, Pin 10)
RX       | TX (GPIO14, Pin 8)

Important:

- TX ↔ RX (cross connection)
- Use 5V power, not 3.3V (sensor may not work properly)

2. Enable Serial Interface on Raspberry Pi

Run:

sudo raspi-config

Go to:

Interface Options → Serial Port

- Disable login shell over serial → No
- Enable serial port hardware → Yes

Then reboot:

sudo reboot

3. Check Serial Port

After reboot:

ls /dev/serial*

You should see something like:

/dev/serial0

4. Install Required Libraries

Use a virtual environment (not recommended):

python3 -m venv fp_env
source fp_env/bin/activate

Install libraries:

pip3 install pyserial adafruit-circuitpython-fingerprint
pip3 install pyfingerprint
pip3 install pyserial
sudo usermod -a -G dialout pi
sudo usermod -a -G dialout $USER


5. How the Sensor Works (Quick Mental Model)

The R305:

1. Captures fingerprint image
2. Converts → template
3. Stores internally (like a database)
4. Matching is done inside the sensor

So Raspberry Pi just sends commands like:

- Capture
- Store
- Search

6. Full Working Code

This code:

- Initializes sensor
- Checks if finger is placed
- Captures fingerprint
- Searches database
- Prints result

import time
import serial
import adafruit_fingerprint

# Initialize UART
uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

# Initialize fingerprint sensor
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Check sensor
if finger.verify_password():
    print("Fingerprint sensor detected!")
else:
    print("Sensor not found")
    exit()

def get_fingerprint():
    print("Waiting for finger...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Image taken")

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image")
        return False

    print("Searching...")

    if finger.finger_search() != adafruit_fingerprint.OK:
        print("No match found")
        return False

    print("Match found!")
    print("ID:", finger.finger_id)
    print("Confidence:", finger.confidence)

    return True

while True:
    get_fingerprint()
    time.sleep(2)

7. Enrolling a Fingerprint (VERY IMPORTANT)

Before matching works, you must store fingerprints.

def enroll_finger(location):
    print("Place finger...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Remove finger...")
    time.sleep(2)

    print("Place same finger again...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        return False

    if finger.create_model() != adafruit_fingerprint.OK:
        return False

    if finger.store_model(location) != adafruit_fingerprint.OK:
        return False

    print("Stored at ID:", location)
    return True

Call it like:

enroll_finger(1)

8. Debugging (Step-by-Step)

Step 1: Check Serial Port

ls /dev/serial0

If not present → serial not enabled.

Step 2: Check Wiring

- TX ↔ RX swapped?
- Proper GND?
- Using 5V?

Step 3: Minimal Test Code

import serial

ser = serial.Serial("/dev/serial0", 57600)
print("Serial OK")

If this fails → UART issue.

Step 4: Sensor Detection Test

if finger.verify_password():
    print("Sensor working")
else:
    print("Sensor NOT detected")

Step 5: Check Baud Rate

Default is 57600.

If not working, try:

baudrate=115200

Common Issues

“Sensor not found”

- Wrong TX/RX
- Serial disabled
- Wrong port

“No match found”

- No fingerprints enrolled
- Poor finger placement

“Image conversion failed”

- Dirty sensor
- Low voltage
- Loose wires

9. Mental Model (Important for Exams)

Think of it like:

Raspberry Pi → (commands) → R305
R305 → (result) → Raspberry Pi

NOT:

Pi doing image processing

Instead:

Sensor does everything internally
How it looks
[Raw Image Buffer] --> image_2_tz() --> [Template Zone 1] / [Template Zone 2]
                             |
                      create_model() --> Permanent Database
                             |
                      finger_search() --> Compare TZ1 to Database