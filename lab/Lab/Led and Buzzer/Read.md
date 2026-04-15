1. Hardware Required
- Raspberry Pi (any model with GPIO pins)
- 3 LEDs (different colors recommended)
- 3 resistors (220Ω – 330Ω)
- Breadboard and jumper wires

2. Connections
LED  | GPIO Pin | Resistor | Notes
LED1 | GPIO17   | 220Ω     | Connect long leg (+) to GPIO through resistor, short leg (-) to GND
LED2 | GPIO27   | 220Ω     | Same as above
LED3 | GPIO22   | 220Ω     | Same as above

Circuit:
GPIO17 ----[220Ω]----> LED1 (anode)
GPIO27 ----[220Ω]----> LED2 (anode)
GPIO22 ----[220Ω]----> LED3 (anode)
All LED cathodes -> GND

* Make sure resistors are in series with LEDs to prevent burning them.
* Use the physical pins on the Raspberry Pi as needed (GPIO17 → Pin 11, GPIO27 → Pin 13, GPIO22 → Pin 15).

3. Python Setup
1. Enable GPIO in Raspberry Pi (already available by default).
2. Install gpiozero:

pip3 install gpiozero (optional)
sudo apt update
sudo apt install python3-gpiozero

4. Python Code
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

5. How it Works
1. gpiozero.LED(pin) initializes an LED object.
2. .on() and .off() control the LED.
3. Functions:
   - blink_in_order(): Lights LEDs from first to last.
   - blink_reverse_order(): Lights LEDs from last to first.
   - blink_random(): Picks a random LED and blinks it.
4. try...except KeyboardInterrupt ensures LEDs turn off if you stop the program.

6. Notes
- Adjust delay to make blinking faster or slower.
- Random blinking uses random.choice() to pick a LED.
- Sequence can be extended for more LEDs by adding to the leds list.



Here’s a complete step-by-step guide for interfacing 1 LED and 1 buzzer with a Raspberry Pi, such that the buzzer alarms when the LED goes off.

1. Hardware Required
- Raspberry Pi (any model with GPIO pins)
- 1 LED
- 1 buzzer (active buzzer recommended)
- 1 resistor (220Ω for LED)
- Breadboard and jumper wires

2. Connections
Component | GPIO Pin | Notes
LED       | GPIO17   | Anode (+) → GPIO through 220Ω resistor, cathode (-) → GND
Buzzer    | GPIO27   | Positive (+) → GPIO, negative (-) → GND

Circuit:
GPIO17 ----[220Ω]----> LED (+)
LED (-) ----------------> GND

GPIO27 ----> Buzzer (+)
Buzzer (-) ----------------> GND

* Make sure the LED has a resistor in series.
* Use an active buzzer (sounds when voltage applied) for simplicity.

3. Python Setup
1. Ensure gpiozero is installed:

pip3 install gpiozero

2. Python standard library time will be used for delays.

4. Python Code
from gpiozero import LED, Buzzer
from time import sleep

# Initialize components
led = LED(17)
buzzer = Buzzer(27)

try:
    while True:
        # Turn LED on for 3 seconds
        led.on()
        print("LED is ON, buzzer is silent")
        buzzer.off()
        sleep(3)
        
        # Turn LED off for 3 seconds
        led.off()
        print("LED is OFF, buzzer ALARM!")
        buzzer.on()
        sleep(3)

except KeyboardInterrupt:
    print("Program stopped by user")
    led.off()
    buzzer.off()

5. How It Works
1. LED(17) initializes the LED on GPIO17.
2. Buzzer(27) initializes the buzzer on GPIO27.
3. led.on() turns the LED on; led.off() turns it off.
4. buzzer.on() triggers the buzzer; buzzer.off() silences it.
5. When the LED goes off, the buzzer is turned on.
6. try...except KeyboardInterrupt ensures safe shutdown.

6. Notes
- You can adjust the sleep() duration to control how long the LED stays on or off.
- For a passive buzzer, you would need to generate a tone using PWM, but an active buzzer is simpler for this use case.
- You can also add a button or sensor to control the LED dynamically if needed.