
Components Required

- Raspberry Pi
- MQ-3 Alcohol Sensor Module (with D0 pin)
- Jumper wires

Step 1: Connections (VERY IMPORTANT)

MQ-3 Pin | Raspberry Pi
VCC      | 5V (Pin 2 or 4)
GND      | GND (Pin 6)
D0       | GPIO17 (Pin 11)

You can use any GPIO, but GPIO17 is standard for labs

Step 2: Install Library

Use gpiozero

pip install gpiozero

Step 3: COMPLETE WORKING CODE

from gpiozero import DigitalInputDevice
from time import sleep

sensor = DigitalInputDevice(17)

print("Alcohol Sensor Initialized...")
print("Waiting for readings...\n")

while True:
    if sensor.value == 1:
        print("Alcohol Detected!")
    else:
        print("No Alcohol Detected")
    sleep(1)

Step 4: How It Works (quick explanation)

- MQ-3 module has a comparator (LM393)
- It compares alcohol level with a threshold
- Output:
  - 1 (HIGH) → Alcohol present
  - 0 (LOW) → No alcohol

Raspberry Pi just reads it like a digital switch

Step 5: VERY IMPORTANT (Calibration)

There is a blue potentiometer on the sensor:

Adjust it like this:

1. Power the sensor
2. Wait ~20–30 seconds (warm-up)
3. Turn the knob slowly
4. Observe LED on module:
   - LED ON → Alcohol detected
   - LED OFF → No alcohol

Set threshold properly before running code

Debugging (If it doesn’t work)

1. Always HIGH / Always LOW?

- Adjust potentiometer
- This is the most common issue

2. Check GPIO pin

Make sure:

sensor = DigitalInputDevice(17)

Matches your wiring

3. Check wiring

- VCC → 5V (NOT 3.3V)
- Common GND required

4. Test GPIO manually

from gpiozero import Button

sensor = Button(17)

while True:
    print(sensor.is_pressed)

Optional (Better Output Format)

from gpiozero import DigitalInputDevice
from time import sleep

sensor = DigitalInputDevice(17)

while True:
    status = "Alcohol Detected!" if sensor.value else "No Alcohol"
    print("Status:", status)
    sleep(1)

Final Summary (What to say in exam)

- MQ-3 gives analog + digital output
- Digital output (D0) uses onboard comparator
- Raspberry Pi reads HIGH/LOW via GPIO
- No ADC required in this mode