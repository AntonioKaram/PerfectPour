import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom pin-numbering scheme)
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo (pin 18)
servo_pin = 18

# Set up pin 18 as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM frequency for the servo (50Hz is typical for servos)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz = 20ms period

# Start PWM running on pin 18, with a duty cycle of 0 (which means the servo is not yet moving)
pwm.start(0)

# Function to set servo position using pulse width (in milliseconds)
def set_pulse_width(pulse_width_ms, duration):
    # Convert the pulse width in milliseconds to duty cycle percentage
    duty_cycle = (pulse_width_ms / 20.0) * 100  # 20ms is the total period (50Hz)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(duration)  # Keep the signal on for the required duration
    pwm.ChangeDutyCycle(0)  # Stop sending the signal to prevent jitter

try:
    # 1. Set to 0 degrees (pulse width = 1 ms)
    print("Setting to 0 degrees")
    set_pulse_width(1.0, 1)  # Move to 0 degrees with 1ms pulse width, hold for 1 second

    # 2. Slowly move to maximum rotation (180 degrees, 2 ms pulse width)
    print("Slowly moving to 180 degrees")
    for pulse_width in range(100, 201, 5):  # 100 = 1.0ms, 200 = 2.0ms (increment in small steps)
        set_pulse_width(pulse_width / 100.0, 0.05)  # Smooth slow movement to max

    # 3. Quickly move to 30 degrees (pulse width ~ 1.25 ms)
    print("Quickly moving to 30 degrees")
    set_pulse_width(1.25, 0.1)  # Fast move to 30 degrees with 1.25ms pulse width

    # 4. Quickly move back to 0 degrees
    print("Quickly moving to 0 degrees")
    set_pulse_width(1.0, 0.1)  # Fast move back to 0 degrees with 1ms pulse width

    # 5. Quickly move to maximum rotation (180 degrees)
    print("Quickly moving to 180 degrees")
    set_pulse_width(2.0, 0.1)  # Fast move to max with 2ms pulse width

finally:
    # Cleanup after the program is finished
    pwm.stop()
    GPIO.cleanup()
