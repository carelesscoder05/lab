from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time

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

try:
    lcd.clear()
    
    # Line 1
    lcd.write_string("Hello World")
    
    # Line 2
    lcd.cursor_pos = (1, 0)
    lcd.write_string("LCD Working")

    time.sleep(10)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close()
    GPIO.cleanup()