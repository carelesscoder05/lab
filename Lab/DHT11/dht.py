import Adafruit_DHT
import time

# Choose sensor type: DHT11 or DHT22
sensor = Adafruit_DHT.DHT11  # change to DHT22 if needed
pin = 4  # GPIO pin connected to DATA

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature}°C | Humidity: {humidity}%")
    else:
        print("Read failed, retrying...")
    
    time.sleep(2)  # wait 2 seconds before next attempt