
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

# Use Raspberry Pi v4 PWM pins
servo1 = Servo(12, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

top_linear = Servo(17, pin_factory=factory)
bottom_linear = Servo(27, pin_factory=factory)


top_linear.min()
bottom_linear.min()
