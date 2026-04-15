import time
import random

def simulate_distance():
    distance = 20   # starting distance
    direction = 1   # 1 = increasing, -1 = decreasing

    try:
        while True:
            # Simulate random sensor failure
            if random.random() < 0.1:
                print("Sensor not detected")
                time.sleep(1)
                continue

            # Random noise
            noise = random.uniform(-0.5, 0.5)

            # Change direction randomly (even before 50)
            if random.random() < 0.2:
                direction *= -1

            # Also enforce hard bounds
            if distance >= 100:
                direction = -1
            elif distance <= 5:
                direction = 1

            # Update distance
            distance += direction * random.uniform(1, 3)

            simulated_distance = distance + noise

            print(f"Distance: {simulated_distance:.2f} cm")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user")

simulate_distance()