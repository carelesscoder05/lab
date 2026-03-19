import RPi.GPIO as GPIO
import time

# GPIO pin mapping
S0 = 23
S1 = 24
S2 = 27
S3 = 22
OUT = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup([S0, S1, S2, S3], GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

# Frequency scaling = 20%
GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.LOW)

def get_frequency():
    start = time.time()
    count = 0
    while time.time() - start < 0.1:
        if GPIO.input(OUT) == GPIO.HIGH:
            count += 1
            while GPIO.input(OUT) == GPIO.HIGH:
                pass
    return count

def read_color():
    # Red
    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.LOW)
    time.sleep(0.1)
    red = get_frequency()

    # Blue
    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.HIGH)
    time.sleep(0.1)
    blue = get_frequency()

    # Green
    GPIO.output(S2, GPIO.HIGH)
    GPIO.output(S3, GPIO.HIGH)
    time.sleep(0.1)
    green = get_frequency()

    return red, green, blue

try:
    while True:
        r, g, b = read_color()
        print("R:", r, " G:", g, " B:", b)

        if r < g and r < b:
            print("Detected Color: RED")
        elif g < r and g < b:
            print("Detected Color: GREEN")
        elif b < r and b < g:
            print("Detected Color: BLUE")
        else:
            print("Detected Color: UNKNOWN")

        print("----------------------")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
