Step 1 — Verify Object Creation

from gpiozero import MotionSensor

try:
    pir = MotionSensor(17)
    print("PIR object created successfully")
except Exception as e:
    print("Error initializing PIR:", e)

If this fails:
- Library issue
- GPIO access issue (permissions)

Step 2 — Check Raw Sensor State

from gpiozero import MotionSensor
import time

pir = MotionSensor(17)

print("Observing raw PIR values (0 = no motion, 1 = motion)")
print("Wait ~30 seconds for sensor stabilization...")

time.sleep(30)

try:
    while True:
        print("Raw value:", int(pir.value))
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopped")

Interpretation:
Output Pattern  → Meaning
Always 0        → No signal → wiring / power issue
Always 1        → Stuck HIGH → sensitivity/delay too high
Changes (0 ↔ 1) → Sensor working

Step 3 — Check Event Triggering

from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(17)

def debug_motion():
    print("DEBUG: Motion event triggered")

def debug_no_motion():
    print("DEBUG: No motion event triggered")

pir.when_motion = debug_motion
pir.when_no_motion = debug_no_motion

print("Move in front of sensor to test events...")
pause()

If:
- Raw values change but no events → config/timing issue
- Events work → system is fine

Step 4 — Check Timing Behavior

from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(17)

print("Testing timing...")

def motion():
    print("Motion START")

def no_motion():
    print("Motion END")

pir.when_motion = motion
pir.when_no_motion = no_motion

pause()

Observe:
- Does “Motion END” come late? → Adjust potentiometer on sensor

Step 5 — Full Debug Script (All-in-One)

from gpiozero import MotionSensor
from signal import pause
import time

print("Initializing PIR sensor...")

try:
    pir = MotionSensor(17)
    print("PIR initialized successfully")
except Exception as e:
    print("Initialization failed:", e)
    exit()

print("Stabilizing sensor (30 sec)...")
time.sleep(30)

print("--- RAW VALUE CHECK ---")
for _ in range(20):
    print("Value:", int(pir.value))
    time.sleep(0.5)

print("--- EVENT CHECK ---")

def motion():
    print("EVENT: Motion detected")

def no_motion():
    print("EVENT: No motion")

pir.when_motion = motion
pir.when_no_motion = no_motion

print("Monitoring events... Press Ctrl+C to stop")
pause()

Common Problems + Diagnosis

Problem: Always 0
- Wrong wiring (OUT pin incorrect)
- No power
- Dead sensor

Problem: Always 1
- Sensitivity too high
- Delay knob maxed
- Sensor saturated (too close movement)

Problem: Random noise
- Unstable power supply
- Loose wires
- No warm-up time

Problem: No events but value changes
- Callback not attached properly
- Program exiting early (missing pause())

Key Debug Insight

Always debug in this order:
1. Initialization
2. Raw value (pir.value)
3. Event callbacks
4. Timing behavior