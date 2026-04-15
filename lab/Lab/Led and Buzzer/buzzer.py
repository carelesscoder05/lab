from gpiozero import LED, Buzzer
from time import sleep

# Initialize components
led = LED(17)
buzzer = Buzzer(27)

try:
    while True:
        # Turn LED on for 3 seconds
        led.on()
        print("LED is ON, buzzer is silent")
        buzzer.off()
        sleep(3)
        
        # Turn LED off for 3 seconds
        led.off()
        print("LED is OFF, buzzer ALARM!")
        buzzer.on()
        sleep(3)

except KeyboardInterrupt:
    print("Program stopped by user")
    led.off()
    buzzer.off()