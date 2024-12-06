from time import sleep
from threading import Thread
import pigpio
import RPi.GPIO as GPIO # type: ignore

# Initialize pigpio
pi = pigpio.pi()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon. Ensure `pigpiod` is running.")

# GPIO Pins for the servos
SERVO1_PIN = 12
SERVO2_PIN = 13

backgate_low = 2
backgate_high = 3

frontgate_low = 4
frontgate_high = 14

GPIO.setup(backgate_low, GPIO.OUT)
GPIO.setup(backgate_high, GPIO.OUT)
GPIO.setup(frontgate_low, GPIO.OUT)
GPIO.setup(frontgate_high, GPIO.OUT)

GPIO.output(backgate_low, GPIO.LOW)
GPIO.output(backgate_high, GPIO.LOW)
GPIO.output(frontgate_low, GPIO.LOW)
GPIO.output(frontgate_high, GPIO.LOW)

# Calibration values from datasheet
SERVO_CALIBRATION = {
    'MIN': 500,    # Minimum pulse width in microseconds
    'MAX': 2500,   # Maximum pulse width in microseconds
    'CENTER': 1500 # Neutral (center) pulse width in microseconds
}

def GPIO_move(in0, in1, duration):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    
    sleep(duration)
    
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)
    
def GPIO_stop(in0, in1):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)

def calculate_pulse_width(position, calibration):
    """
    Calculate the pulse width for the given normalized position.
    - `position`: Normalized value (-1.0 to 1.0) for servo angle.
    """
    if position < -1.0 or position > 1.0:
        raise ValueError("Position must be between -1.0 and 1.0")
    
    if position <= 0:
        return int(calibration['CENTER'] + position * (calibration['CENTER'] - calibration['MIN']))
    else:
        return int(calibration['CENTER'] + position * (calibration['MAX'] - calibration['CENTER']))

def smooth_move_servo(pin, start_position, target_position, calibration, steps=50, delay=0.01):
    """
    Smoothly move a servo from start_position to target_position.
    - `start_position` and `target_position` are normalized (-1.0 to 1.0).
    """
    start_pulse = calculate_pulse_width(start_position, calibration)
    target_pulse = calculate_pulse_width(target_position, calibration)
    step_size = (target_pulse - start_pulse) / steps

    for step in range(steps + 1):
        pulse = start_pulse + step * step_size
        pi.set_servo_pulsewidth(pin, int(pulse))
        sleep(delay)

def reset_servos():
    """
    Reset servos to the center position (neutral).
    """
    print("Resetting servos to center position...")
    smooth_move_servo(SERVO1_PIN, -1, 0, SERVO_CALIBRATION)
    smooth_move_servo(SERVO2_PIN, 1, 0, SERVO_CALIBRATION)
    print("Servos reset.")

def control_rotational_servos():
    """
    Interactive control for rotational servos.
    """
    current_position1 = 0.0 # Start at center
    current_position2 = 0.0 # Start at center

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

        thread1 = Thread(target=smooth_move_servo, args=(SERVO1_PIN, current_position1, target_position1, SERVO_CALIBRATION))
        thread2 = Thread(target=smooth_move_servo, args=(SERVO2_PIN, current_position2, target_position2, SERVO_CALIBRATION))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Update current positions
        current_position1 = target_position1
        current_position2 = target_position2

        print("Movement complete.")

# Main Program Loop
try:
    while True:
        print("\nOptions:")
        print("1. Control Rotational Servos (r)")
        print("2. Reset Servos (reset)")
        print("3. Exit (q)")

        choice = input("Enter your choice: ").strip().lower()

        if choice == 'r':
            # control_rotational_servos()
            GPIO_move(backgate_low, backgate_high, 2)
        elif choice == 'reset':
            reset_servos()
        elif choice == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")
finally:
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()
