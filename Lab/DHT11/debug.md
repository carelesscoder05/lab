You are verifying 4 layers:

1. GPIO works?
2. Pin receives signal?
3. Library reads correctly?
4. Sensor itself alive?

STEP 1 — Verify GPIO is Working

Goal:

Check if your Pi can read HIGH/LOW signals

Code:

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN = 4

GPIO.setup(PIN, GPIO.IN)

print("Reading GPIO state... Press Ctrl+C to stop")

try:
    while True:
        state = GPIO.input(PIN)
        print("PIN STATE:", state)
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

What to do:

Step-by-step:

Identify the pins on your Pi
Physical Pin 1 → 3.3V (VCC)
Physical Pin 6 → GND
Physical Pin 7 → GPIO4 (the pin you are testing)

Disconnect the DHT sensor DATA wire from GPIO4.

Test HIGH (1)
Take a jumper wire and touch one end to GPIO4 (Pin 7) and the other end to 3.3V (Pin 1).
Your Python script should now print: PIN STATE: 1.

Test LOW (0)
Move the jumper from 3.3V to GND (Pin 6), keeping the other end on GPIO4 (Pin 7).
Your Python script should now print: PIN STATE: 0.

If this fails:

Problem = GPIO / wiring / wrong pin numbering

STEP 2 — Check Pull-Up Behavior (needs DHT attached)

Why:

DHT11 requires DATA line HIGH by default

Code (same as above)

What to expect:

- When idle → should mostly read 1 (HIGH)

If always 0:

Missing 10kΩ pull-up resistor

STEP 3 — Raw Signal Detection (Important)

Now check if DHT11 is even sending pulses

Code:

import RPi.GPIO as GPIO
import time

PIN = 4

GPIO.setmode(GPIO.BCM)

def detect_signal():
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(PIN, GPIO.IN)

    count = 0
    while GPIO.input(PIN) == 1:
        count += 1
        if count > 10000:
            print("No response from sensor")
            return

    print("Sensor responded!")

detect_signal()
GPIO.cleanup()

Meaning:

- If you see “No response”
  Sensor not connected / dead / wrong pin

- If “Sensor responded!”
  Hardware is working → move to next step

STEP 4 — Add Retry Debug Wrapper

DHT11 often fails randomly → you must retry

Debug Code:

import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
pin = 4

def read_dht_debug(retries=5):
    for i in range(retries):
        print(f"Attempt {i+1}...")

        humidity, temperature = Adafruit_DHT.read(sensor, pin)

        if humidity is not None and temperature is not None:
            print("SUCCESS")
            print(f"Temp: {temperature}°C | Humidity: {humidity}%")
            return True
        else:
            print("Read failed, retrying...")
            time.sleep(2)

    print("All retries failed")
    return False

while True:
    read_dht_debug()
    print("----------------------")
    time.sleep(3)

What this tells you:

- Works sometimes → timing issue (normal for DHT11)
- Never works → deeper problem

STEP 5 — Check Permissions

Run:

sudo python3 your_script.py

If it works only with sudo:
GPIO permission issue

STEP 6 — Check Library Installation

Test:

import Adafruit_DHT
print("Library loaded successfully")

If error:

pip3 install Adafruit_DHT

STEP 7 — Force Lower-Level Read (More Reliable)

Sometimes read() fails silently. Use:

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print(humidity, temperature)

This internally retries multiple times.

STEP 8 — Hardware Sanity Checks

If everything above passes but still no data:

Check:

- Power = 3.3V (NOT 5V)
- Correct pin:
  BCM 4 = Physical Pin 7
- Try different GPIO pin
- Try another DHT11 sensor

Common Failure Patterns (Recognize Quickly)

Symptom        Likely Cause
Always None    Wiring / dead sensor
Works randomly Normal (DHT11 limitation)
Always 0/0     Wrong pin / no pull-up
No response    Sensor not powered

Key Insight (Important)

DHT11 is:

- Slow
- Timing-sensitive
- Not very reliable