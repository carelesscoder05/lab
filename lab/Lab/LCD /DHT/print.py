import time
import random
import RPi.GPIO as GPIO
from RPLCD import CharLCD

GPIO.setmode(GPIO.BCM)

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16, rows=2,
    pin_rs=26,
    pin_rw=None,
    pin_e=19,
    pins_data=[13, 6, 5, 11]
)

temp = 25
hum = 60

try:
    while True:
        # Randomly simulate sensor failure (20% chance)
        if random.randint(1, 5) == 1:
            print("Sensor not detected")

            lcd.clear()
            lcd.write_string("Sensor Error")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Check DHT11")

            time.sleep(2)
            continue

        # Simulate temperature change
        temp += random.choice([-1, 0, 1])
        hum += random.choice([-2, -1, 0, 1, 2])

        # Keep values realistic
        temp = max(20, min(35, temp))
        hum = max(40, min(80, hum))

        # Print debug output
        print(f"Temp={temp}C Humidity={hum}%")

        # Display on LCD
        # print(f"[DEBUG] Temp={temp:.1f}C Humidity={hum:.1f}%")

        lcd.clear()
        lcd.write_string(f"Temp:{temp:.1f}C")

        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Hum:{hum:.1f}%")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lcd.clear()
    GPIO.cleanup()