import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIR_PIN = 17

GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Warming up PIR sensor (60 sec)...")
time.sleep(60)

print("PIR ready")

try:
    while True:
        if GPIO.input(PIR_PIN) == 1:
            print("Motion detected")
            time.sleep(2)
        else:
            print("No motion")
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()