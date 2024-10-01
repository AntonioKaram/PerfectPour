import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin 18 for PWM (servo control)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (typical for servos)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with 0 duty cycle
pwm.start(0)

# Function to rotate the servo to a specified angle (0 to 180 degrees)
def set_angle(angle, speed=0.135):
    # Calculate duty cycle for the given angle (map from 2% to 12%)
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    
    # Calculate time based on speed and angle difference
    rotation_time = speed * abs(angle - current_angle) / 60  # sec/degree * degrees
    time.sleep(rotation_time)
    
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Stop sending signal

# Current position of the servo (track position to calculate rotation time)
current_angle = 0

# Function to gradually move the servo to a specified angle
def move_slowly(target_angle, step=1, delay=0.01):
    global current_angle
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, step):
            set_angle(angle, speed=0.135)  # Adjust speed if necessary
            time.sleep(delay)
    elif current_angle > target_angle:
        for angle in range(current_angle, target_angle - 1, -step):
            set_angle(angle, speed=0.135)
            time.sleep(delay)
    current_angle = target_angle

try:
    # Start by moving to 0 degrees (slowly)
    print("Moving to 0 degrees...")
    move_slowly(0, step=1, delay=0.01)
    
    # Slowly move to maximum rotation (180 degrees)
    print("Moving to max rotation (180 degrees)...")
    move_slowly(180, step=1, delay=0.02)
    
    # Quickly move back to half rotation (90 degrees)
    print("Quickly moving back to half rotation (90 degrees)...")
    set_angle(90, speed=0.07)  # Faster speed for quicker movement
    current_angle = 90
    time.sleep(0.5)
    
    # Quickly move back to 0 degrees
    print("Quickly moving back to 0 degrees...")
    set_angle(0, speed=0.07)
    current_angle = 0
    time.sleep(0.5)
    
    # Quickly move back to max rotation (180 degrees)
    print("Quickly moving back to max rotation...")
    set_angle(180, speed=0.07)
    current_angle = 180
    time.sleep(0.5)

finally:
    # Stop PWM and clean up
    pwm.stop()
    GPIO.cleanup()
