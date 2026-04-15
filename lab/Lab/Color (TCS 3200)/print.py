import time
import random

try:
    while True:
        # Randomly decide whether to detect a color or be undecidable
        if random.random() < 0.15:  # ~15% chance of undecidable
            print("Color not detected")
        else:
            # Generate mock RGB values
            # Pick one color to dominate
            dominant_color = random.choice(["Red", "Green", "Blue"])
            if dominant_color == "Red":
                r = random.randint(180, 255)
                g = random.randint(0, 120)
                b = random.randint(0, 120)
            elif dominant_color == "Green":
                r = random.randint(0, 120)
                g = random.randint(180, 255)
                b = random.randint(0, 120)
            else:  # Blue
                r = random.randint(0, 120)
                g = random.randint(0, 120)
                b = random.randint(180, 255)

            print(f"Red: {r} | Green: {g} | Blue: {b}")

        # Random delay to simulate sensor reading interval
        time.sleep(random.uniform(0.5, 1.5))

except KeyboardInterrupt:
    print("\nSimulation stopped.")