import RPi.GPIO as GPIO
import time

# Set up the GPIO mode and pin
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM frequency for the servo (50Hz is typical)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

try:
    # # Slowly increase the angle (0 to 180 degrees)
    # for duty in range(0, 110):  # Duty cycle from 2.5% to 12.5%
    #     pwm.ChangeDutyCycle(duty / 10.0)  # Convert to percentage
    #     time.sleep(0.1)  # Small delay between steps
    # time.sleep(1)

    # # Slowly decrease the angle (180 to 0 degrees)
    # for duty in range(110, 0, -1):
    #     pwm.ChangeDutyCycle(duty / 10.0)
    #     time.sleep(0.1)
    # time.sleep(1)
    
    pwm.ChangeDutyCycle(0)
    time.sleep(1)
    
    pwm.ChangeDutyCycle(0.5)
    time.sleep(1)
    
    pwm.ChangeDutyCycle(1)
    time.sleep(1)
    
    pwm.ChangeDutyCycle(5)
    time.sleep(1)
    
    pwm.ChangeDutyCycle(10)
    time.sleep(1)
    
    pwm.ChangeDutyCycle(100)
    time.sleep(1)
    

finally:
    pwm.stop()
    GPIO.cleanup()
