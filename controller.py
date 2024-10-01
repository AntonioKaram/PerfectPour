import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom pin-numbering scheme)
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo (pin 18)
servo_pin = 18

# Set up pin 18 as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM frequency for the servo (50Hz is typical for servos)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM running on pin 18, with a duty cycle of 0 (servo not moving initially)
pwm.start(0)

# Function to rotate the servo to a specific angle (between 0 and 180 degrees)
def set_angle(angle):
    # Duty cycle ranges from 2% (0 degrees) to 12% (180 degrees)
    duty = 2.5 + (angle / 180.0) * 10.0  # Adjusting for servo-specific range
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Give time for the servo to move
    pwm.ChangeDutyCycle(0)  # Stop sending signal to hold the position

# Function to rotate the servo continuously for full rotations
def rotate_continuous(rotations, fast=True):
    if fast:
        speed_factor = 0.5  # Fast speed
    else:
        speed_factor = 2  # Slow speed
    
    for _ in range(rotations * 2):  # 2 half rotations = 1 full rotation
        set_angle(180)
        time.sleep(speed_factor)  # Control speed
        set_angle(0)
        time.sleep(speed_factor)  # Control speed

try:
    # Start with the servo pointing straight up (0 degrees)
    print("Starting at 0 degrees (straight up)")
    set_angle(0)
    time.sleep(2)

    # Rotate 180 degrees to point straight down
    print("Rotating to 180 degrees (straight down)")
    set_angle(180)
    time.sleep(2)

    # Perform 1 fast full rotation
    print("Performing 1 fast full rotation")
    rotate_continuous(rotations=1, fast=True)
    time.sleep(2)

    # Perform 1 slow full rotation
    print("Performing 1 slow full rotation")
    rotate_continuous(rotations=1, fast=False)

finally:
    # Cleanup after the program is finished
    pwm.stop()
    GPIO.cleanup()
