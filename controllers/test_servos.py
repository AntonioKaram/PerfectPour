import time
import pigpio
import signal
import sys

# Constants
SERVO1_PIN = 12  # GPIO pin for first servo
SERVO2_PIN = 13  # GPIO pin for second servo

# Calibration values (adjust these for your servos)
SERVO1_CALIBRATION = {
    'min_pulse': 500,
    'max_pulse': 2500,
    'center_pulse': 1500
}

SERVO2_CALIBRATION = {
    'min_pulse': 500,
    'max_pulse': 2500,
    'center_pulse': 1500
}

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Error: Unable to connect to pigpio daemon")
    sys.exit(1)

def cleanup(signum, frame):
    """Cleanup GPIO on exit"""
    print("\nCleaning up...")
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

def calculate_pulse_width(position, calibration):
    """
    Convert position (-1 to 1) to pulse width
    """
    min_pulse = calibration['min_pulse']
    max_pulse = calibration['max_pulse']
    center_pulse = calibration['center_pulse']
    
    if position < 0:
        return center_pulse + ((center_pulse - min_pulse) * position)
    else:
        return center_pulse + ((max_pulse - center_pulse) * position)

def synchronized_servo_move(target_position, current_position=0):
    """
    Move both servos in synchronized opposite directions.
    target_position: -1.0 to 1.0 where 0 is center
    current_position: starting position of servos
    """
    STEP_DELAY = 0.02  # 20ms delay between steps
    STEP_SIZE = 0.05   # Move in 0.05 increments for smoothness
    
    # Calculate direction and steps
    steps = abs(int((target_position - current_position) / STEP_SIZE))
    step_dir = 1 if target_position > current_position else -1
    
    for i in range(steps):
        pos = current_position + (step_dir * STEP_SIZE * i)
        # Calculate pulse widths - note opposite signs for each servo
        servo1_pulse = calculate_pulse_width(pos, SERVO1_CALIBRATION)
        servo2_pulse = calculate_pulse_width(-pos, SERVO2_CALIBRATION)
        
        # Set both servos simultaneously
        pi.set_servo_pulsewidth(SERVO1_PIN, servo1_pulse)
        pi.set_servo_pulsewidth(SERVO2_PIN, servo2_pulse)
        time.sleep(STEP_DELAY)
    
    # Final position
    servo1_pulse = calculate_pulse_width(target_position, SERVO1_CALIBRATION)
    servo2_pulse = calculate_pulse_width(-target_position, SERVO2_CALIBRATION)
    pi.set_servo_pulsewidth(SERVO1_PIN, servo1_pulse)
    pi.set_servo_pulsewidth(SERVO2_PIN, servo2_pulse)

# Global variables for tracking servo positions
current_position = 0.0

# Reset both servos to center
print("Resetting servos to center position...")
synchronized_servo_move(0)
print("Servos reset.")

# Set servos to starting position
synchronized_servo_move(-1.0)
current_position = -1.0

# Main program loop
run = True

while run:
    print("\n----------------------------------------------")
    print("-----------------TEST MODULE------------------")
    print("----------------------------------------------")
    print(f"Current Position: {current_position:.2f}")
    print("\nOptions:")
    print("1. Tilt Forward (+0.2) (f)")
    print("2. Tilt Backward (-0.2) (b)")
    print("3. Reset to Center (c)")
    print("4. Full Pour Position (p)")
    print("5. Return to Start (s)")
    print("6. Exit (q)")
    
    choice = input("Enter choice: ").lower()
    
    if choice in ['f', '1']:
        target = min(current_position + 0.2, 1.0)
        synchronized_servo_move(target, current_position)
        current_position = target
        
    elif choice in ['b', '2']:
        target = max(current_position - 0.2, -1.0)
        synchronized_servo_move(target, current_position)
        current_position = target
        
    elif choice in ['c', '3']:
        synchronized_servo_move(0, current_position)
        current_position = 0
        print("Servos centered")
        
    elif choice in ['p', '4']:
        synchronized_servo_move(1.0, current_position)
        current_position = 1.0
        print("Moving to pour position")
        
    elif choice in ['s', '5']:
        synchronized_servo_move(-1.0, current_position)
        current_position = -1.0
        print("Moving to start position")
        
    elif choice in ['q', '6']:
        synchronized_servo_move(0, current_position)  # Return to center before exit
        print("Exiting...")
        cleanup(None, None)
        run = False