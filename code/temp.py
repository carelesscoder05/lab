import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT22   # CHANGE if DHT11
gpio_pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)

    if humidity is not None and temperature is not None:
        if -40 < temperature < 80 and 0 <= humidity <= 100:
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Humidity: {humidity:.2f} %")
            print("-" * 30)
        else:
            print("Out-of-range values detected, ignoring...")
    else:
        print("Failed to read from sensor")

    time.sleep(3)