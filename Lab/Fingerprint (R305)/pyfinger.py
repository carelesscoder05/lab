from pyfingerprint.pyfingerprint import PyFingerprint
import time

# Initialize sensor
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("Wrong password")
except Exception as e:
    print("Sensor init failed:", e)
    exit(1)

print("Fingerprint Sensor Ready")

def enroll():
    print("Place finger for enrollment...")
    while not f.readImage():
        pass
    f.convertImage(0x01)

    if f.searchTemplate()[0] >= 0:
        print("Fingerprint already exists")
        return

    print("Remove finger")
    time.sleep(2)

    print("Place same finger again...")
    while not f.readImage():
        pass
    f.convertImage(0x02)

    f.createTemplate()
    pos = f.storeTemplate()
    print("Enrolled at position:", pos)

def verify():
    print("Place finger to verify...")
    while not f.readImage():
        pass
    f.convertImage(0x01)

    result = f.searchTemplate()
    if result[0] >= 0:
        print("Match found at ID:", result[0])
        print("Accuracy:", result[1])
    else:
        print("No match found")

while True:
    print("\n1. Enroll Fingerprint")
    print("2. Verify Fingerprint")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        enroll()
    elif choice == '2':
        verify()
    elif choice == '3':
        break
    else:
        print("Invalid choice")







        
# from pyfingerprint.pyfingerprint import PyFingerprint
# import time

# try:
#     # Initialize sensor
#     f = PyFingerprint('/dev/serial0', 57600)

#     if not f.verifyPassword():
#         raise ValueError('Wrong sensor password!')

#     print("Sensor initialized")
#     print("Currently stored templates:", f.getTemplateCount())

#     # -------------------------------
#     # ENROLL PHASE
#     # -------------------------------
#     print("\n--- ENROLL NEW FINGER ---")
#     input("Place finger to enroll and press Enter...")

#     # Wait for finger
#     while not f.readImage():
#         pass

#     # Convert to characteristics (buffer 1)
#     f.convertImage(0x01)

#     # Check if already exists
#     result = f.searchTemplate()
#     position = result[0]

#     if position >= 0:
#         print("Finger already exists at position:", position)
#     else:
#         print("Remove finger...")
#         time.sleep(2)

#         input("Place the SAME finger again and press Enter...")

#         while not f.readImage():
#             pass

#         # Convert to characteristics (buffer 2)
#         f.convertImage(0x02)

#         # Compare both scans
#         if f.compareCharacteristics() == 0:
#             raise Exception("Fingers do not match")

#         # Create template
#         f.createTemplate()

#         # Store template
#         position = f.storeTemplate()
#         print("Finger enrolled at position:", position)

#     # -------------------------------
#     # MATCH PHASE
#     # -------------------------------
#     print("\n--- MATCH FINGER ---")

#     while True:
#         print("\nWaiting for finger...")

#         while not f.readImage():
#             pass

#         f.convertImage(0x01)

#         result = f.searchTemplate()
#         position = result[0]
#         accuracy = result[1]

#         if position >= 0:
#             print("Match found!")
#             print("Position:", position)
#             print("Accuracy score:", accuracy)
#         else:
#             print("No match found")

#         time.sleep(2)

# except Exception as e:
#     print("Error:", e)




