from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Initialize LCD in 4-bit mode
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
    lcd.cursor_pos = (1, 0)  # Second row
    lcd.write_string("Raspberry Pi LCD")
    time.sleep(10)  # Display for 10 seconds
finally:
    lcd.clear()
    GPIO.cleanup()






# import RPi.GPIO as GPIO
# import time

# # Pin setup (BCM)
# RS = 26
# E  = 19
# D4 = 13
# D5 = 6
# D6 = 5
# D7 = 11

# GPIO.setmode(GPIO.BCM)

# pins = [RS, E, D4, D5, D6, D7]
# for p in pins:
#     GPIO.setup(p, GPIO.OUT)

# def pulse_enable():
#     GPIO.output(E, True)
#     time.sleep(0.001)
#     GPIO.output(E, False)
#     time.sleep(0.001)

# def send_nibble(data):
#     GPIO.output(D4, (data >> 0) & 1)
#     GPIO.output(D5, (data >> 1) & 1)
#     GPIO.output(D6, (data >> 2) & 1)
#     GPIO.output(D7, (data >> 3) & 1)
#     pulse_enable()

# def send_byte(data, mode):
#     GPIO.output(RS, mode)
#     send_nibble(data >> 4)
#     send_nibble(data & 0x0F)
#     time.sleep(0.002)

# def lcd_init():
#     send_byte(0x33, 0)
#     send_byte(0x32, 0)
#     send_byte(0x28, 0)
#     send_byte(0x0C, 0)
#     send_byte(0x06, 0)
#     send_byte(0x01, 0)

# def lcd_string(message):
#     for char in message:
#         send_byte(ord(char), 1)

# try:
#     lcd_init()
#     lcd_string("HELLO")
# finally:
#     GPIO.cleanup()