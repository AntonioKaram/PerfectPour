from time import sleep
from threading import Thread
import pigpio

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon. Ensure `pigpiod` is running.")

# GPIO Pins for the servos
SERVO1_PIN = 12
SERVO2_PIN = 13

# Individual servo calibration
SERVO1_CALIBRATION = {
    'MIN': 800,
    'MAX': 2300,
    'CENTER': 1190
}

SERVO2_CALIBRATION = {
    'MIN': 800,
    'MAX': 2300,
    'CENTER': 1190
}

# Then modify calculate_pulse_width to accept calibration values
def calculate_pulse_width(position, calibration):
    if position < -1.0 or position > 1.0:
        raise ValueError("Position must be between -1.0 and 1.0")
        
    if position <= 0:
        return int(calibration['CENTER'] + position * (calibration['CENTER'] - calibration['MIN']))
    else:
        return int(calibration['CENTER'] + position * (calibration['MAX'] - calibration['CENTER']))


# Servo initialization
pi.set_servo_pulsewidth(SERVO1_PIN, calculate_pulse_width(-1.0, SERVO1_CALIBRATION))
pi.set_servo_pulsewidth(SERVO2_PIN, calculate_pulse_width(-1.0, SERVO2_CALIBRATION))


def smooth_move_servo(pin, start_position, target_position, calibration, steps=50, delay=0.02):
    """
    Move a servo smoothly from start_position to target_position.
    - `start_position` and `target_position` are normalized values (-1.0 to 1.0).
    - `calibration` is the calibration dictionary for the servo.
    - `steps` determines the granularity of the movement.
    - `delay` is the time between each step.
    """
    start_pulse = calculate_pulse_width(start_position, calibration)
    target_pulse = calculate_pulse_width(target_position, calibration)
    step_size = (target_pulse - start_pulse) / steps

    for step in range(steps + 1):
        pulse = start_pulse + step * step_size
        pi.set_servo_pulsewidth(pin, int(pulse))
        sleep(delay)

def control_rotational_servos():
    # Set initial position to -1
    current_position = -1.0
    
    while True:
        try:
            # Get user input for new position (-1.0 to 1.0)
            new_position = float(input("Enter position (-1.0 to 1.0, or 'q' to quit): "))
            if new_position < -1.0 or new_position > 1.0:
                print("Position must be between -1.0 and 1.0")
                continue
                
            # Move both servos to new position
            smooth_move_servo(SERVO1_PIN, current_position, new_position, SERVO1_CALIBRATION)
            smooth_move_servo(SERVO2_PIN, current_position, new_position, SERVO2_CALIBRATION)
            current_position = new_position
            
        except ValueError:
            print("Invalid input. Please enter a number between -1.0 and 1.0")
        except KeyboardInterrupt:
            # Return servos to -1 position on exit
            smooth_move_servo(SERVO1_PIN, current_position, -1.0, SERVO1_CALIBRATION)
            smooth_move_servo(SERVO2_PIN, current_position, -1.0, SERVO2_CALIBRATION)

def reset_servos():
    """
    Reset both servos to the center (neutral) position.
    """
    print("Resetting servos to center position...")
    smooth_move_servo(SERVO1_PIN, -1, -1, SERVO1_CALIBRATION)
    smooth_move_servo(SERVO2_PIN, -1, -1, SERVO2_CALIBRATION)
    print("Servos reset.")

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
            pi.stop()
        case _:
            print("Invalid option. Please try again.")
