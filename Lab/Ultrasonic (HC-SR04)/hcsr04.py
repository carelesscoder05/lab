import RPi.GPIO as GPIO
import time

# Pin configuration
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Ensure TRIG is LOW
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Send 10us pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for ECHO to go HIGH
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for ECHO to go LOW
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Time difference
    pulse_duration = pulse_end - pulse_start

    # Distance calculation
    distance = pulse_duration * 17150  # (34300 / 2)

    return round(distance, 2)

try:
    print("Measuring Distance... Press Ctrl+C to stop")

    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    GPIO.cleanup()