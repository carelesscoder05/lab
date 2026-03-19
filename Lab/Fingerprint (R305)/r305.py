import time
import serial
import adafruit_fingerprint

# Initialize Serial & Sensor
uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Check sensor
if finger.verify_password():
    print(" Sensor detected!")
else:
    print(" Sensor not found")
    exit()

# Enroll fingerprint (only once)
def enroll_single(location=1):
    print("Place your finger to enroll...")

    # Step 1: first scan
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Image captured. Remove finger.")
    time.sleep(2)

    # Step 2: second scan
    print("Place the same finger again...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert first image")
        return False
    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        print("Failed to convert second image")
        return False

    # Create model & store
    if finger.create_model() != adafruit_fingerprint.OK:
        print("Failed to create model")
        return False
    if finger.store_model(location) != adafruit_fingerprint.OK:
        print("Failed to store fingerprint")
        return False

    print("Fingerprint enrolled successfully!")
    return True

# Check fingerprint
def check_finger():
    print("Place your finger for recognition...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to convert image")
        return

    if finger.finger_search() == adafruit_fingerprint.OK:
        print("Finger recognized! Access granted.")
    else:
        print("Finger not recognized! Access denied.")

# Main Program
# Enroll once at ID 1
enroll_single(location=1)

# Loop to check finger
while True:
    check_finger()
    time.sleep(2)











# import time
# import serial
# import adafruit_fingerprint

# # --------------------------
# # Initialize UART & Fingerprint Sensor
# # --------------------------
# uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)
# finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# # Check if sensor is connected
# if finger.verify_password():
#     print("Fingerprint sensor detected!")
# else:
#     print("Sensor not found. Check wiring and serial port.")
#     exit()

# # --------------------------
# # Enroll Fingerprint Function
# # --------------------------
# def enroll_finger(location=None):
#     if location is None:
#         try:
#             location = int(input("Enter ID to store fingerprint (1-127): "))
#         except ValueError:
#             print("Invalid ID")
#             return False

#     print(f"\n--- Enrolling Fingerprint at ID {location} ---")

#     # Step 1: first scan
#     print("Place your finger...")
#     while finger.get_image() != adafruit_fingerprint.OK:
#         pass
#     print("Image captured. Remove finger.")
#     time.sleep(2)

#     # Step 2: second scan
#     print("Place the same finger again...")
#     while finger.get_image() != adafruit_fingerprint.OK:
#         pass

#     if finger.image_2_tz(1) != adafruit_fingerprint.OK:
#         print("Failed to convert first image")
#         return False
#     if finger.image_2_tz(2) != adafruit_fingerprint.OK:
#         print("Failed to convert second image")
#         return False

#     # Step 3: create model
#     if finger.create_model() != adafruit_fingerprint.OK:
#         print("Failed to create model")
#         return False

#     # Step 4: store model
#     if finger.store_model(location) != adafruit_fingerprint.OK:
#         print("Failed to store fingerprint")
#         return False

#     print(f"Fingerprint enrolled successfully at ID {location}!")
#     return True

# # --------------------------
# # Check Fingerprint Function
# # --------------------------
# def check_finger():
#     print("\nPlace your finger for recognition...")

#     while finger.get_image() != adafruit_fingerprint.OK:
#         pass

#     if finger.image_2_tz(1) != adafruit_fingerprint.OK:
#         print("Failed to convert image")
#         return

#     if finger.finger_search() == adafruit_fingerprint.OK:
#         print(f"Finger recognized! ID: {finger.finger_id}, Confidence: {finger.confidence}")
#     else:
#         print("Finger not recognized! Access denied.")

# # --------------------------
# # Main Menu Loop
# # --------------------------
# def main_menu():
#     while True:
#         print("\n--- Fingerprint Menu ---")
#         print("1. Enroll Fingerprint")
#         print("2. Check Fingerprint")
#         print("3. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             enroll_finger()
#         elif choice == "2":
#             check_finger()
#         elif choice == "3":
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice. Try again.")

# if __name__ == "__main__":
#     main_menu()