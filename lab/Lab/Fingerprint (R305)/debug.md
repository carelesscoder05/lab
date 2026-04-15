
Check Serial Port on Raspberry Pi

R305 communicates over UART. First, make sure the port exists:

ls /dev/serial0

- If you see /dev/serial0 → good.
- If not → serial interface is not enabled.

Enable it:

sudo raspi-config

- Interface Options → Serial Port
- Disable login shell → No
- Enable serial port hardware → Yes
- Reboot:

sudo reboot

Test Basic Serial Communication

Before using the fingerprint library, make sure UART works:

import serial

try:
    ser = serial.Serial("/dev/serial0", 57600, timeout=1)
    print("Serial port opened successfully")
    ser.close()
except Exception as e:
    print("Serial error:", e)

- If this fails → wiring or serial setup problem
- If this works → proceed

Check Sensor Password (Basic Library Test)

Use the library’s verify_password function to see if the sensor responds:

import serial
import adafruit_fingerprint

uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

if finger.verify_password():
    print("Sensor detected!")
else:
    print("Sensor not responding. Check wiring and baud rate")

- detected → sensor is alive
- not responding → could be TX/RX swapped, wrong voltage, or wrong serial port

Test Image Capture

Check if the sensor can detect a finger:

print("Place your finger...")
while True:
    result = finger.get_image()
    if result == adafruit_fingerprint.OK:
        print("Image captured")
        break
    elif result == adafruit_fingerprint.NOFINGER:
        print(".", end="", flush=True)
    else:
        print(f"Error capturing image: {result}")

- If it never captures → finger not on sensor, dirty sensor, or wiring/voltage issue

Test Image Conversion

After capturing, convert image to template (TZ1):

if finger.image_2_tz(1) == adafruit_fingerprint.OK:
    print("Image converted successfully")
else:
    print("Failed to convert image")

- Conversion fails → low voltage, loose connection, or faulty sensor

Test Fingerprint Search

If a fingerprint is already enrolled, test matching:

if finger.finger_search() == adafruit_fingerprint.OK:
    print(f"Match found! ID: {finger.finger_id}, Confidence: {finger.confidence}")
else:
    print("No match found")

- No match → wrong finger, or nothing enrolled at ID 1

Check Voltage and Wiring

- VCC → 5V (Raspberry Pi pin 2 or 4)
- GND → GND (Pin 6)
- TX ↔ RX (cross connection)
- RX ↔ TX

Common mistake: TX→TX, RX→RX. Must be swapped.

Debugging Baud Rate

- Default R305 baud: 57600
- If the sensor does not respond, try 115200:

uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

Minimal “All-in-One” Debug Script

This script prints step-by-step responses:

import serial
import adafruit_fingerprint
import time

uart = serial.Serial("/dev/serial0", 57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

print("Checking sensor...")
if finger.verify_password():
    print("Sensor OK")
else:
    print("Sensor not responding")

print("Testing image capture...")
res = finger.get_image()
if res == adafruit_fingerprint.OK:
    print("Image captured")
elif res == adafruit_fingerprint.NOFINGER:
    print("No finger detected")
else:
    print(f"Error: {res}")

print("Testing conversion...")
if finger.image_2_tz(1) == adafruit_fingerprint.OK:
    print("Image converted")
else:
    print("Conversion failed")

print("Testing search...")
if finger.finger_search() == adafruit_fingerprint.OK:
    print(f"Match found! ID: {finger.finger_id}")
else:
    print("No match found")

Run this script step by step to see exactly where it fails.