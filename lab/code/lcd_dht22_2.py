import time
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import Adafruit_DHT

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
sensor = Adafruit_DHT.DHT22
dht_pin = 4   # GPIO4

try:
    while True:

        humidity, temperature = Adafruit_DHT.read_retry(sensor, dht_pin)

        lcd.clear()

        if temperature is not None and humidity is not None:
            lcd.write_string("Temp: {:.1f} C".format(temperature))
            lcd.cursor_pos = (1, 0)   # move to 2nd row
            lcd.write_string("Hum: {:.1f} %".format(humidity))
        else:
            lcd.write_string("Sensor Error")

        time.sleep(2)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close()
    GPIO.cleanup()