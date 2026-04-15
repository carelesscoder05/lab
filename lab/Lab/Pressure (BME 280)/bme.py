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