from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

# Create a PiGPIOFactory instance and set the PWM frequency (default is 50Hz)
factory = PiGPIOFactory()
factory.set_pwm_frequency(50)  # 50 Hz is typically used for servos

# Use hardware PWM pin (e.g., GPIO 18)
servo = Servo(18, pin_factory=factory, min_pulse_width=0.0005, max_pulse_width=0.0025)

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
