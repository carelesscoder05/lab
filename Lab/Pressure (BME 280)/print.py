import random
import time

def simulate_sensor_reading():
    """Simulate a BME280 sensor reading"""
    # 10% chance the sensor is "not detected"
    if random.random() < 0.1:
        return None

    # Generate realistic random values
    temperature = round(random.uniform(20.0, 30.0), 2)  # °C
    pressure = round(random.uniform(990.0, 1030.0), 2)  # hPa
    humidity = round(random.uniform(30.0, 70.0), 2)     # %

    return temperature, pressure, humidity

# Simulate continuous readings
try:
    while True: 
        data = simulate_sensor_reading()

        if data is None:
            print("Sensor not detected!")
        else:
            temperature, pressure, humidity = data
            print(f"Temperature: {temperature} °C, Pressure: {pressure} hPa, Humidity: {humidity} %")

        time.sleep(2)
except KeyboardInterrupt:
    pass