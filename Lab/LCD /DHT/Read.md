1. Connections

A. LCD → Raspberry Pi (Physical Pins)
LCD Pin | Function        | Connect to Pi
VSS     | GND             | Pin 6
VDD     | 5V              | Pin 2
VO      | Contrast        | Pot middle pin
RS      | Register Select | Pin 37 (GPIO 26)
RW      | Write mode      | Pin 9 (GND)
E       | Enable          | Pin 35 (GPIO 19)
D4      | Data            | Pin 33 (GPIO 13)
D5      | Data            | Pin 31 (GPIO 6)
D6      | Data            | Pin 29 (GPIO 5)
D7      | Data            | Pin 23 (GPIO 11)
A       | Backlight +     | Pin 2 (5V) via 330Ω
K       | Backlight -     | Pin 6 (GND)

B. Potentiometer (Contrast Control)
Pot Pin | Connect to
End 1   | 5V (Pin 2)
End 2   | GND (Pin 6)
Middle  | LCD VO (Pin 3)

C. DHT11 → Raspberry Pi
DHT11 Pin | Connect to
VCC       | Pin 1 (3.3V)
DATA      | Pin 11 (GPIO 17)
GND       | Pin 6 (GND)
Note: If using raw sensor, add 10kΩ pull-up resistor (DATA → VCC). Module includes resistor.

2. Install Required Libraries
sudo apt update
sudo apt install python3-pip libgpiod2
pip3 install RPLCD adafruit-circuitpython-dht

3. Working Code
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from RPLCD import CharLCD

# GPIO setup
GPIO.setmode(GPIO.BCM)

# LCD setup
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16, rows=2,
    pin_rs=26,
    pin_rw=None,
    pin_e=19,
    pins_data=[13, 6, 5, 11]
)

# DHT11 setup
dht = adafruit_dht.DHT11(board.D17)

# Main loop
try:
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity

            print(f"[DEBUG] Temp={temp}C Humidity={hum}%")

            lcd.clear()
            lcd.write_string(f"Temp: {temp} C")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Hum: {hum} %")

            time.sleep(2)

        except RuntimeError as e:
            print("[ERROR] Sensor read failed:", e)
            lcd.clear()
            lcd.write_string("Sensor Error")
            time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lcd.clear()
    GPIO.cleanup()

4. Execution Steps
1. Complete all wiring
2. Power ON Raspberry Pi
3. Adjust potentiometer until LCD text is visible
4. Save file: nano dht_lcd.py
5. Run: python3 dht_lcd.py

5. What You Should See
On LCD:
Temp: 28 C
Hum: 65 %

On Terminal:
[DEBUG] Temp=28C Humidity=65%

6. Important Practical Notes
DHT11 Behavior:
- Slow sensor, updates every ~2 seconds
- Occasional read errors normal

LCD Behavior:
- If blank → adjust potentiometer
- If garbage → check D4–D7 order
- If only blocks → initialization issue

Voltage Notes:
- DHT11 works on 3.3V safely
- LCD uses 5V (logic still works with Pi GPIO)

7. Final Mental Model
DHT11 → GPIO → Python → RPLCD → GPIO → LCD → Display
- Sensor provides data
- Pi reads it
- LCD displays it