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