from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

# Create a PiGPIOFactory instance and set the PWM frequency (default is 50Hz)
factory = PiGPIOFactory()

# Use hardware PWM pin (e.g., GPIO 18)
servo = Servo(18, pin_factory=factory, min_pulse_width=0.00009, max_pulse_width=0.002)

try:
    while True:
        servo.min()  # Move to min position
        sleep(1)
        servo.mid()  # Move to mid position
        sleep(1)
        servo.max()  # Move to max position
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
