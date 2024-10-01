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
def set_angle(angle):
    duty = 2 + (angle / 18)  # Map the angle to a duty cycle (2-12 for 0-180 degrees)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Wait for the servo to reach the desired angle
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Stop sending the signal

try:
    # Test rotating the servo to different positions
    print("Rotating to 0 degrees")
    set_angle(0)
    time.sleep(2)

    print("Rotating to 90 degrees")
    set_angle(90)
    time.sleep(2)

    print("Rotating to 180 degrees")
    set_angle(180)
    time.sleep(2)

finally:
    # Cleanup after the program is finished
    pwm.stop()
    GPIO.cleanup()
