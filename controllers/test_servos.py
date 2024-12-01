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
    """
    Interactive control for the rotational servos.
    """
    current_position1 = 0.0  # Start at center position
    current_position2 = 0.0  # Start at center position

    while True:
        print(f"\nCurrent Positions: Servo1: {current_position1:.2f}, Servo2: {current_position2:.2f}")
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

        # Opposite position for Servo2
        target_position2 = -target_position1
        print(f"Moving Servo1 to {target_position1:.2f} and Servo2 to {target_position2:.2f}...")

        thread1 = Thread(target=smooth_move_servo, args=(SERVO1_PIN, current_position1, target_position1, SERVO1_CALIBRATION))
        thread2 = Thread(target=smooth_move_servo, args=(SERVO2_PIN, current_position2, target_position2, SERVO2_CALIBRATION))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Update current positions
        current_position1 = target_position1
        current_position2 = target_position2

        print("Movement complete.")

def reset_servos():
    """
    Reset both servos to the center (neutral) position.
    """
    print("Resetting servos to center position...")
    smooth_move_servo(SERVO1_PIN, -1, -1, SERVO1_CALIBRATION)
    smooth_move_servo(SERVO2_PIN, 0.0, -1, SERVO2_CALIBRATION)
    print("Servos reset.")
    
    
    
servo1_pulse = calculate_pulse_width(-1.0, SERVO1_CALIBRATION)
servo2_pulse = calculate_pulse_width(-1.0, SERVO2_CALIBRATION)

# Set servos to starting position
pi.set_servo_pulsewidth(SERVO1_PIN, servo1_pulse)
pi.set_servo_pulsewidth(SERVO2_PIN, servo2_pulse)

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
