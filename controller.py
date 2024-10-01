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

# Start PWM running on pin 18, with a duty cycle of 0 (which means the servo is not yet moving)
pwm.start(0)

# Function to rotate the servo to a specified angle (0 to 180 degrees)
def set_angle(angle, duration=1):
    duty = 2 + (angle / 18)  # Map the angle to a duty cycle (2-12 for 0-180 degrees)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(duration)  # Wait for the servo to reach the desired angle
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Stop sending the signal

# Function to rotate continuously (for full rotations)
def rotate_continuous(speed, rotations=1):
    period = 1 / speed  # Calculate the time for one full rotation
    for _ in range(rotations * 2):  # 2 half rotations (each from 0 to 180)
        set_angle(180, duration=period / 2)  # Rotate to 180 degrees
        set_angle(0, duration=period / 2)    # Rotate back to 0 degrees

try:
    # Start with servo pointing straight up (0 degrees)
    print("Starting straight up (0 degrees)")
    set_angle(0)
    time.sleep(2)

    # Rotate 180 degrees to point straight down
    print("Rotating to straight down (180 degrees)")
    set_angle(180)
    time.sleep(2)

    # Perform 2 full rotations:
    # 1 fast rotation
    print("Performing 1 fast full rotation")
    rotate_continuous(speed=1, rotations=1)  # Speed=1 full rotation per second
    time.sleep(2)

    # 1 slow rotation
    print("Performing 1 slow full rotation")
    rotate_continuous(speed=0.2, rotations=1)  # Speed=0.2 rotations per second (slow)

finally:
    # Cleanup after the program is finished
    pwm.stop()
    GPIO.cleanup()
