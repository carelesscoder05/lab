import RPi.GPIO as GPIO
import time

# Pin setup (BCM mode)
S2 = 27
S3 = 22
OUT = 17
S0 = 23
S1 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)
GPIO.setup(S0, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

# Set frequency scaling to 20%
GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.LOW)

def count_pulses(duration=0.1):
    start_time = time.time()
    count = 0

    while time.time() - start_time < duration:
        if GPIO.input(OUT) == GPIO.LOW:
            while GPIO.input(OUT) == GPIO.LOW:
                pass
            count += 1

    return count

def get_color():
    # RED
    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.LOW)
    time.sleep(0.1)
    red = count_pulses()

    # BLUE
    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.HIGH)
    time.sleep(0.1)
    blue = count_pulses()

    # GREEN
    GPIO.output(S2, GPIO.HIGH)
    GPIO.output(S3, GPIO.HIGH)
    time.sleep(0.1)
    green = count_pulses()

    return red, green, blue

try:
    while True:
        r, g, b = get_color()
        print(f"Red: {r} | Green: {g} | Blue: {b}")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()