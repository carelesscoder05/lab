When the **BME280** doesn’t work, the mistake can be at *any layer* (wiring → OS → I²C → Python → sensor data).
So debugging should move **bottom-up**, not randomly.

---

#  Step-by-Step Debugging Strategy

Think in 4 layers:

```
Hardware → I²C Bus → OS Interface → Python Code
```

We’ll verify each layer independently.

---

#  STEP 1 — Hardware Sanity Check

###  Check wiring

* VCC → 3.3V (NOT 5V)
* GND → GND
* SDA → GPIO2
* SCL → GPIO3

### ✔ Quick electrical check

* Sensor heating up?  bad sign
* Loose jumper wires? very common issue

---

#  STEP 2 — Check I²C is enabled

Run:

```bash
ls /dev/i2c-*
```

###  Expected:

```
/dev/i2c-1
```

###  If missing:

Enable I²C using `raspi-config` (as explained earlier)

---

#  STEP 3 — Detect device on bus

```bash
i2cdetect -y 1
```

###  Expected output:

```
0x76  OR  0x77
```

---

###  Case 1: Nothing shows

Problem is **hardware or wiring**

---

###  Case 2: Shows but unstable

 Loose wires / power issue

---

#  STEP 4 — Low-Level Python Debug (RAW I²C)

Now we test communication **without BME library**

## 🔧 Debug Script 1: Check device presence

```python
import smbus2

bus = smbus2.SMBus(1)

for addr in range(0x03, 0x78):
    try:
        bus.write_quick(addr)
        print(f"Device found at: {hex(addr)}")
    except:
        pass
```

###  Expected:

```
Device found at: 0x76
```

---

##  Debug Script 2: Read chip ID

BME280 has a **fixed chip ID = 0x60**

```python
import smbus2

bus = smbus2.SMBus(1)
address = 0x76  # try 0x77 also

chip_id = bus.read_byte_data(address, 0xD0)

print(f"Chip ID: {hex(chip_id)}")
```

---

###  Expected:

```
0x60
```

---

###  If not 0x60:

| Output | Meaning                       |
| ------ | ----------------------------- |
| 0x58   | It’s **BMP280** (no humidity) |
| Error  | Address wrong / wiring issue  |

---

#  STEP 5 — Minimal BME280 Test

Now test library only:

```python
import smbus2
import bme280

port = 1
address = 0x76

bus = smbus2.SMBus(port)

try:
    calibration_params = bme280.load_calibration_params(bus, address)
    print("Calibration loaded successfully")
except Exception as e:
    print("Calibration failed:", e)
```

---

###  If this fails:

* Wrong address
* Sensor not responding correctly

---

#  STEP 6 — Full Sensor Read Debug
```python
import smbus2
import bme280

port = 1
address = 0x76

bus = smbus2.SMBus(port)

try:
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

    print("Temperature:", data.temperature)
    print("Pressure:", data.pressure)
    print("Humidity:", data.humidity)

except Exception as e:
    print("Error reading sensor:", e)
```

---

#  Common Failure Cases (Important)

###  “No such file /dev/i2c-1”

 I²C not enabled

---

###  “Remote I/O error”



* Wrong address
* Loose wiring
* Sensor not powered

---

###  Values = 0 or weird



* Calibration not loaded
* Fake/clone sensor
* Power instability

---

###  Humidity always 0

 You probably have:
**BMP280** (no humidity)

---

#  Final Debug Flow (Memorize This)

```
1. Wiring correct?
2. /dev/i2c-1 exists?
3. i2cdetect shows address?
4. Chip ID = 0x60?
5. Calibration loads?
6. Data reads correctly?
```

 If you follow this sequence, you’ll **always isolate the issue quickly**.

---


