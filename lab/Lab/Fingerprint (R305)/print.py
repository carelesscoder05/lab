import time
import random

def simulate_sensor():
    # Randomly simulate sensor detection
    if random.random() < 0.3:  # 10% chance sensor fails
        print("Sensor not detected!")
        return False
    print("Sensor detected!")
    return True

def wait_for_finger():
    print("Waiting for finger...", end="", flush=True)
    for _ in range(random.randint(3, 6)):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(" Finger placed!")

def capture_image():
    print("Capturing fingerprint image...", end="", flush=True)
    time.sleep(1)
    print(" Image captured!")

def convert_to_template():
    print("Converting image to template...", end="", flush=True)
    time.sleep(1)
    print(" Conversion done!")

def search_database():
    print("Searching fingerprint database...", end="", flush=True)
    time.sleep(1)
    # Randomly simulate match or no match
    if random.random() < 0.7:  # 70% chance match
        finger_id = random.randint(1, 5)
        confidence = random.randint(80, 100)
        print(f" Match found! ID: {finger_id}, Confidence: {confidence}")
    else:
        print(" No match found!")

# Main loop
while True:
    print("\n--- Fingerprint Sensor Simulation ---")
    if not simulate_sensor():
        time.sleep(2)
        continue
    wait_for_finger()
    capture_image()
    convert_to_template()
    search_database()
    time.sleep(2)