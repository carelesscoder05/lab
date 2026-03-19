from gpiozero import LED
from time import sleep
import random

# Initialize LEDs
led1 = LED(17)
led2 = LED(27)
led3 = LED(22)

leds = [led1, led2, led3]

def blink_in_order(delay=0.5):
    print("Blinking in order...")
    for led in leds:
        led.on()
        sleep(delay)
        led.off()

def blink_reverse_order(delay=0.5):
    print("Blinking in reverse order...")
    for led in reversed(leds):
        led.on()
        sleep(delay)
        led.off()

def blink_random(delay=0.5, times=5):
    print("Blinking randomly...")
    for _ in range(times):
        led = random.choice(leds)
        led.on()
        sleep(delay)
        led.off()

# Main loop
try:
    while True:
        blink_in_order()
        sleep(0.5)
        blink_reverse_order()
        sleep(0.5)
        blink_random()
        sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped by user")
    for led in leds:
        led.off()