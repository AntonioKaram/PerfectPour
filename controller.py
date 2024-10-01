from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

# Use PiGPIOFactory for precise control
Servo.pin_factory = PiGPIOFactory()

# Use a hardware PWM pin (e.g., GPIO 18)
# Customize pulse width range and PWM frequency if needed
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025, pwm_frequency=100)

try:
    while True:
        servo.min()  # Move to min position
        sleep(0.5)
        servo.mid()  # Move to mid position
        sleep(0.5)
        servo.max()  # Move to max position
        sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped")
