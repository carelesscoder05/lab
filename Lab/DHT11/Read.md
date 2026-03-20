
1. Components Required

- Raspberry Pi (any model with GPIO)
- DHT11 sensor
- 10kΩ resistor (pull-up) ---> not used at all
- Breadboard + jumper wires

2. Wiring (Very Important)

DHT11 has 3 or 4 pins depending on module:

If using raw DHT11 (4 pins):

Pin 1 → VCC (3.3V)
Pin 2 → DATA (GPIO)
Pin 3 → NC (Not connected)
Pin 4 → GND

If using module (3 pins):

VCC → 3.3V
DATA → GPIO4 (Pin 7)
GND → GND

Pull-up resistor:

- Connect 10kΩ resistor between VCC and DATA

GPIO Pin Mapping (Recommended)

- DATA → GPIO4 (Physical Pin 7)

3. Enable GPIO + Install Libraries

Update system:

sudo apt update
sudo apt upgrade

Install required packages:

sudo apt install python3-pip python3-dev build-essential
sudo apt install libgpiod2
sudo apt install python3-rpi.gpio python3-pip
sudo apt install python3-adafruit-dht

pip3 install adafruit-circuitpython-dht
pip3 install Adafruit_DHT
pip3 install RPi.GPIO



If install fails:

sudo pip3 install Adafruit_DHT

4. Understanding How It Works

DHT11:

- Uses single-wire digital protocol
- Returns:
  - Temperature (°C)
  - Humidity (%)

Library handles:

- Timing-sensitive signal decoding
- Retry logic (sensor is unreliable sometimes)

5. Python Code (Complete)

import Adafruit_DHT 
import time

sensor = Adafruit_DHT.DHT11 
pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read(sensor, pin)

    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print("-------------------------")
    else:
        print("Failed to retrieve data from sensor")

    time.sleep(2)

# import adafruit_dht
# import board

# dht = adafruit_dht.DHT11(board.D4)

# try:
#     temperature = dht.temperature
#     humidity = dht.humidity
#     print(temperature, humidity)
# except RuntimeError:
#     print("Sensor error")

6. Run the Program

python3 dht11.py

7. Expected Output

Temperature: 28°C
Humidity: 65%
-------------------------

8. Common Issues (Very Important)

1. Failed to retrieve data

- DHT11 is slow + unreliable
- Fix:
  - Wait 2 seconds between reads
  - Check wiring
  - Ensure pull-up resistor

2. Permission issues

Run with sudo:

sudo python3 dht11.py

3. Wrong GPIO numbering

- Code uses BCM (GPIO4)
- NOT physical pin number

9. Optional: Use GPIO Zero (Cleaner Approach)

Install:

pip3 install gpiozero

Code:

from gpiozero import CPUTemperature
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read(sensor, pin)

    if humidity and temperature:
        print(f"Temp: {temperature}°C | Humidity: {humidity}%")
    
    time.sleep(2)

If resistor is used:

3.3V (Pi) ----+---- VCC (Sensor)
              |
             [10kΩ]
              |
DATA (Sensor) ---> GPIO4 (Pi)
GND (Sensor)  ---> GND (Pi)
