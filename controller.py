from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

# Create a PiGPIOFactory instance and set the PWM frequency (default is 50Hz)
factory = PiGPIOFactory()

# Use hardware PWM pin (e.g., GPIO 18)
servo = Servo(18, pin_factory=factory, min_pulse_width=0.00008, max_pulse_width=0.0023)

def move_servo_smoothly(start_position, end_position, duration):
    steps = 1000  # Number of steps to take
    step_delay = duration / steps  # Time per step
    step_size = (end_position - start_position) / steps  # Increment for each step
    
    for i in range(steps + 1):
        position = start_position + i * step_size
        if position < 0:
            servo.min()  # Move to min if position is less than 0
        elif position > 1:
            servo.max()  # Move to max if position is greater than 1
        else:
            servo.value = position  # Set the servo to the interpolated position
        sleep(step_delay)

try:
    while True:
        print("Moving from min to max")
        move_servo_smoothly(0, 1, 2)  # Move from 0 (min) to 1 (max) over 2 seconds
        sleep(1)

        print("Moving from max to min")
        move_servo_smoothly(1, 0, 2)  # Move from 1 (max) to 0 (min) over 2 seconds
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
