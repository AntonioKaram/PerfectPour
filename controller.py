import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom pin-numbering scheme)
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo (pin 18 - PCM_CLK)
servo_pin = 18

# Set up pin 18 as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM frequency for the servo (50Hz for typical servo control)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz PWM signal

# Start PWM on pin 18 with a duty cycle of 0 (servo off initially)
pwm.start(0)

# Function to rotate the servo to a specified angle (0 to 180 degrees)
def set_angle(angle):
    # Convert the angle to a duty cycle (2 to 12 for 0° to 180°)
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Give it time to reach the position
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Stop sending PWM signal

try:
    # Move to 0° to start
    print("Moving to 0 degrees")
    set_angle(0)
    time.sleep(2)

    # Slowly move to max rotation (180 degrees)
    print("Slowly moving to max rotation (180 degrees)")
    for angle in range(0, 181, 1):  # Gradually increase angle from 0 to 180
        set_angle(angle)
        time.sleep(0.05)  # Slow transition

    time.sleep(1)  # Pause for 1 second

    # Quickly move back to 30 degrees
    print("Quickly moving back to 30 degrees")
    set_angle(30)
    time.sleep(0.5)

    # Quickly move back to 0 degrees
    print("Quickly moving back to 0 degrees")
    set_angle(0)
    time.sleep(0.5)

    # Quickly move back to max rotation (180 degrees)
    print("Quickly moving to max rotation (180 degrees)")
    set_angle(180)
    time.sleep(0.5)

finally:
    # Cleanup after program finishes
    pwm.stop()
    GPIO.cleanup()
