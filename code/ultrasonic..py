import RPi.GPIO as GPIO
import time

# GPIO Mode
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

try:
    while True:
        # Trigger pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for echo start
        while GPIO.input(ECHO) == 0:
            start_time = time.time()

        # Wait for echo end
        while GPIO.input(ECHO) == 1:
            end_time = time.time()

        duration = end_time - start_time

        # Distance calculation
        distance = (duration * 34300) / 2

        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()


#     VCC → 5V (Pin 2 or 4) ❌ NOT 3.3V

# GND → GND

# TRIG → GPIO23

# ECHO → GPIO24 via voltage divider

# Sensor facing an object within 2–400 cm