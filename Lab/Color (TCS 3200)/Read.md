Interfacing the TCS3200 with a Raspberry Pi is slightly more involved than sensors like DHT11 because it outputs a frequency signal, not digital data. So you’re essentially measuring pulse frequency → mapping to RGB intensity.

Core Idea (before wiring)

The TCS3200 has:

- Photodiodes with filters: Red, Green, Blue
- It converts light intensity → square wave frequency
- You select which color to measure using pins S2, S3
- You scale output frequency using S0, S1

So the flow is:

Select color → Measure frequency → Convert to intensity → Repeat for RGB

Pin Configuration

TCS3200 Pin | Function          | Pi GPIO (BCM) | Pi Physical Pin
VCC         | Power             | —             | Pin 1 (3.3V)
GND         | Ground            | —             | Pin 6
OUT         | Frequency output  | GPIO17        | Pin 11
S0          | Frequency scaling | GPIO23        | Pin 16
S1          | Frequency scaling | GPIO24        | Pin 18
S2          | Color select      | GPIO27        | Pin 13
S3          | Color select      | GPIO22        | Pin 15

Important:

- Some TCS3200 modules are 5V → ensure output is safe (use voltage divider if needed)
- Prefer 3.3V operation if your module supports it

Step 1: Install Required Library

sudo apt update
sudo apt install python3-rpi.gpio

Step 2: Full Python Code

import RPi.GPIO as GPIO
import time

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
    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.LOW)
    time.sleep(0.1)
    red = count_pulses()

    GPIO.output(S2, GPIO.LOW)
    GPIO.output(S3, GPIO.HIGH)
    time.sleep(0.1)
    blue = count_pulses()

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

Step 3: How This Code Works (Important Understanding)

1. Frequency Scaling

GPIO.output(S0, HIGH)
GPIO.output(S1, LOW)

- Sets output to 20% scaling
- Prevents extremely high frequency (hard to measure)

2. Color Selection Logic

S2 | S3 | Color
0  | 0  | Red
0  | 1  | Blue
1  | 1  | Green

So:

GPIO.output(S2, LOW)
GPIO.output(S3, LOW)

→ selects red filter

3. Pulse Counting = Frequency Measurement

count += 1

- Counts how many pulses occur in 0.1 sec
- Higher count → higher intensity

Essentially:

Intensity ∝ Frequency ∝ Pulse count

Step 4: Interpreting Output

Example:

Red: 120 | Green: 45 | Blue: 30

→ Object is reddish

Step 5: Calibration (VERY IMPORTANT)

Raw values are not actual RGB (0–255).

You should:

1. Measure values for:
   - White surface
   - Black surface

2. Normalize:

normalized = (value - min) / (max - min) * 255

Debugging Approach (Step-by-step)

If it doesn’t work:

Step 1: Check Power

- LED on sensor ON?
- If not → wiring issue

Step 2: Check Output Pin

while True:
    print(GPIO.input(OUT))

- Should toggle rapidly (0/1)
- If always 0 or 1 → sensor not working / wrong wiring

Step 3: Test Frequency Scaling

Try:

GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.HIGH)

→ Highest frequency mode  
If counts still zero → issue in OUT pin

Step 4: Slow Down Counting

Increase duration:

count_pulses(1.0)

Step 5: Use Multimeter / Logic Analyzer (if available)

- Check OUT pin waveform

Common Mistakes

- Using 5V output directly → may damage GPIO
- Not setting S0/S1 → no output
- Not waiting after switching filters
- Counting too fast → inaccurate readings