import random
import time

try:
    while True:
        # 20% chance of sensor failure
        if random.random() < 0.2:
            print("Sensor not detected, retrying...")
        else:
            # Simulated readings
            temperature = random.randint(20, 30)  # °C
            humidity = random.randint(40, 70)     # %
            print(f"Temperature: {temperature}°C | Humidity: {humidity}%")
        
        time.sleep(2)

except KeyboardInterrupt:
   pass