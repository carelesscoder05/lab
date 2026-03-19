import time
import board
import adafruit_dht
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.cleanup()

# -------- LCD SETUP --------
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16,
    rows=2,
    pin_rs=25,
    pin_e=24,
    pins_data=[23, 17, 18, 22]
)

# -------- DHT22 SETUP --------
dhtDevice = adafruit_dht.DHT22(board.D4)

try:
    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            lcd.clear()
            lcd.write_string(f"Temp: {temperature:.1f} C")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Hum: {humidity:.1f} %")

        except RuntimeError:
            lcd.clear()
            lcd.write_string("Sensor Error")

        time.sleep(2)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close()
    GPIO.cleanup()


# pip3 install adafruit-circuitpython-dht
# pip3 install RPLCD
# pip3 install RPi.GPIO

# DHT22 +   → 3.3V (Pin 1)
# DHT22 -   → GND  (Pin 6)
# DHT22 OUT → GPIO4 (Pin 7)


# | LCD Pin | Function      | Connect To              |
# | ------- | ------------- | ----------------------- |
# | 1       | GND           | GND (Pin **9**)         |
# | 2       | VCC           | 5V (Pin **2**)          |
# | 3       | Contrast (V0) | Middle of Potentiometer |
# | 4       | RS            | GPIO25 (**Pin 22**)     |
# | 5       | RW            | GND (Pin **14**)        |
# | 6       | EN            | GPIO24 (**Pin 18**)     |
# | 11      | D4            | GPIO23 (**Pin 16**)     |
# | 12      | D5            | GPIO17 (**Pin 11**)     |
# | 13      | D6            | GPIO18 (**Pin 12**)     |
# | 14      | D7            | GPIO22 (**Pin 15**)     |
# | 15      | LED+          | 5V (Pin **4**)          |
# | 16      | LED−          | GND (Pin **20**)        |
