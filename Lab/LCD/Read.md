Complete step-by-step guide to interface a 16×2 LCD with a Raspberry Pi and display messages, including wiring and potentiometer for contrast control.

Components Required:
- Raspberry Pi (any model with GPIO)
- 16×2 LCD (HD44780 controller)
- 10 kΩ potentiometer
- Jumper wires
- Breadboard
- 330 Ω resistor (optional, for backlight)

Step 1: Understanding the LCD Pins
A standard 16×2 LCD has 16 pins:
Pin | Name    | Function
1   | VSS     | GND
2   | VDD/VCC | +5V
3   | VO      | Contrast adjustment (connect to potentiometer)
4   | RS      | Register Select (0=Command, 1=Data)
5   | RW      | Read/Write (0=Write, 1=Read; usually tied to GND)
6   | E       | Enable pin
7   | D0      | Data bit 0
8   | D1      | Data bit 1
9   | D2      | Data bit 2
10  | D3      | Data bit 3
11  | D4      | Data bit 4
12  | D5      | Data bit 5
13  | D6      | Data bit 6
14  | D7      | Data bit 7
15  | A/LED+  | Backlight + (optional resistor)
16  | K/LED-  | Backlight -

We will use 4-bit mode, connecting only D4–D7 (pins 11–14) for data.

Step 2: Wiring the LCD to Raspberry Pi
Use BCM pin numbering.
LCD Pin | Function        | BCM GPIO | Physical Pin
VSS     | GND             | —        | Pin 6
VDD     | 5V              | —        | Pin 2
VO      | Contrast        | —        | Potentiometer middle pin
RS      | Register Select | GPIO 26  | Pin 37
RW      | GND             | —        | Pin 9
E       | Enable          | GPIO 19  | Pin 35
D4      | Data 4          | GPIO 13  | Pin 33
D5      | Data 5          | GPIO 6   | Pin 31
D6      | Data 6          | GPIO 5   | Pin 29
D7      | Data 7          | GPIO 11  | Pin 23
A       | Backlight +     | —        | Pin 2 via 330Ω
K       | Backlight -     | —        | Pin 6

Potentiometer wiring:
- One end → 5V
- Other end → GND
- Middle wiper → VO (pin 3 of LCD)
Rotating the potentiometer adjusts LCD contrast.

Step 3: Installing Required Python Library
sudo apt update
sudo apt install python3-pip python3-dev python3-smbus
python3 -m venv lcd_env
source lcd_env/bin/activate
pip install RPLCD RPi.GPIO
sudo usermod -aG gpio $USER

Step 4: Python Code to Display Text
from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16, rows=2,
    pin_rs=26, pin_rw=None, pin_e=19,
    pins_data=[13, 6, 5, 11],
    charmap='A00'
)

try:
    lcd.clear()
    lcd.write_string("Hello, World!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Raspberry Pi LCD")
    time.sleep(10)
finally:
    lcd.clear()
    GPIO.cleanup()

Step 5: Testing and Adjusting
1. Run: python3 lcd_test.py
2. If blank, adjust potentiometer for contrast
3. Backlight should be visible; use 330 Ω resistor if needed

Debugging Tips:
- Nothing appears:
  - Check GPIO connections
  - Ensure RPLCD installed
  - Adjust potentiometer
- Partial text:
  - Verify 4-bit mode pins D4–D7
- Backlight not on:
  - Check A/K pins and series resistor

This is a standard approach to interface a 16×2 LCD with Raspberry Pi using 4-bit mode with potentiometer-controlled contrast.