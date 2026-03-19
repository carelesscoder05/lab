import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from RPLCD import CharLCD

# ---------------- GPIO SETUP ----------------
GPIO.setmode(GPIO.BCM)

# ---------------- LCD SETUP ----------------
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16, rows=2,
    pin_rs=26,
    pin_rw=None,
    pin_e=19,
    pins_data=[13, 6, 5, 11]
)

# ---------------- DHT11 SETUP ----------------
dht = adafruit_dht.DHT11(board.D17)

# ---------------- MAIN LOOP ----------------
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