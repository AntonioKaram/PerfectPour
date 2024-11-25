from time import sleep
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from threading import Thread

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

# Set up rotating servos
servo1 = Servo(12, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, initial_value=None)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, initial_value=None)

# Initial positions
servo1.value = 0  # Center position
servo2.value = 0  # Center position


def rotate_to_position(servo, target_position):
    """Smoothly move a servo to a specified position."""
    current_position = servo.value if servo.value is not None else 0
    steps = 50
    step_size = (target_position - current_position) / steps
    step_delay = 0.02  # Adjust as needed for smoother motion

    for step in range(steps + 1):
        position = current_position + step * step_size
        servo.value = max(-1, min(1, position))  # Clamp between -1 and 1
        sleep(step_delay)


def control_rotational_servos():
    """Control servos interactively."""
    while True:
        print(f"\nCurrent Positions: Servo1: {servo1.value}, Servo2: {servo2.value}")
        input_position = input("Enter target position (-1.0 to 1.0) for Servo1 (or 'q' to quit): ")

        if input_position.lower() == 'q':
            print("Exiting control mode.")
            break

        try:
            target_position1 = float(input_position)
            if not -1.0 <= target_position1 <= 1.0:
                raise ValueError("Position out of range.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        target_position2 = -target_position1  # Opposite direction for servo2
        print(f"Moving Servo1 to {target_position1} and Servo2 to {target_position2}...")

        thread1 = Thread(target=rotate_to_position, args=(servo1, target_position1))
        thread2 = Thread(target=rotate_to_position, args=(servo2, target_position2))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        print("Movement complete.")


def reset_servos():
    """Reset both servos to the default positions."""
    rotate_to_position(servo1, 0)
    rotate_to_position(servo2, 0)
    print("Servos reset to the center position.")


# Main program loop
run = True
while run:
    print("\n----------------------------------------------")
    print("-----------------TEST MODULE------------------")
    print("----------------------------------------------")
    print("Options")
    print("1. Control Rotational Servos (r)")
    print("2. Reset Servos (reset)")
    print("3. Exit (q)")

    test = input("Which test do you want to run? ")

    match test:
        case "r":
            control_rotational_servos()
        case "reset":
            reset_servos()
        case "q":
            run = False
            reset_servos()
            GPIO.cleanup()
        case _:
            print("Invalid option. Please try again.")
