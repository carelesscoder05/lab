
1. Hardware Connections (I²C)

BME280 → Raspberry Pi

BME280 Pin | Raspberry Pi Pin
-----------|----------------
VCC        | 3.3V (Pin 1)
GND        | GND (Pin 6)
SCL        | GPIO3 (Pin 5)
SDA        | GPIO2 (Pin 3)

Important:

- Use 3.3V only (NOT 5V)
- Most modules already have pull-up resistors

2. Enable I²C on Raspberry Pi

Run:

sudo raspi-config

- Go to: Interface Options → I2C → Enable

Reboot:

sudo reboot

3. Verify Sensor Detection

Install tools:

sudo apt update
sudo apt install -y i2c-tools

Check:

i2cdetect -y 1

Expected output:

0x76 or 0x77

That’s your BME280 address.

4. Install Required Python Libraries

Recommended approach:

python3 -m venv bme_env (optional)
source bme_env/bin/activate (optional)
pip3 install smbus2 bme280  
sudo usermod -aG i2c $USER

5. Complete Python Code

import smbus2
import bme280

# BME280 default address (change to 0x77 if needed)
port = 1
address = 0x76

bus = smbus2.SMBus(port)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

def read_sensor():
    data = bme280.sample(bus, address, calibration_params)

    temperature = data.temperature
    pressure = data.pressure
    humidity = data.humidity

    print(f"Temperature: {temperature:.2f} °C")
    print(f"Pressure: {pressure:.2f} hPa")
    print(f"Humidity: {humidity:.2f} %")
    print("-" * 30)

if __name__ == "__main__":
    import time
    while True:
        read_sensor()
        time.sleep(2)

6. Run the Program

python3 your_script.py

7. Expected Output

Temperature: 28.45 °C
Pressure: 1008.23 hPa
Humidity: 65.12 %
------------------------------

8. Step-by-Step Debugging (if it fails)

Not detected in i2cdetect:

- Check wiring
- Ensure I²C is enabled
- Try both addresses: 0x76 and 0x77

Permission error:

sudo usermod -aG i2c $USER

Re-login

Wrong readings:

- Ensure stable power (3.3V)
- Check if your module is BME280 (not BMP280 — no humidity)

Module not found:

pip install smbus2 bme280

Deep Understanding (Important Concept)

The BME280 internally:

- Uses calibration coefficients stored in registers
- Raw ADC values are read via I²C
- Library applies compensation formulas

That’s why this line is critical:

calibration_params = bme280.load_calibration_params(...)

Without it → incorrect values.