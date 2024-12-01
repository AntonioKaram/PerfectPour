from time import sleep
import pigpio

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon. Ensure `pigpiod` is running.")

# GPIO Pins for the servos
SERVO1_PIN = 12
SERVO2_PIN = 13

# Servo pulse width range (microseconds)
MIN_PULSE_WIDTH = 500    # Corresponds to -90 degrees
MAX_PULSE_WIDTH = 2500   # Corresponds to +90 degrees
CENTER_PULSE_WIDTH = 1500  # Neutral (0 degrees)

def angle_to_pulse_width(angle):
    """Convert angle (-90 to +90 degrees) to pulse width."""
    # Ensure the angle is within the valid range
    angle = max(-90, min(90, angle))
    # Map angle to pulse width
    pulse_width = MIN_PULSE_WIDTH + (angle + 90) * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 180
    return pulse_width

def set_servo_angle(servo_pin, angle):
    """Set servo to the specified angle."""
    pulse_width = angle_to_pulse_width(angle)
    pi.set_servo_pulsewidth(servo_pin, pulse_width)
    print(f"Moved servo on GPIO {servo_pin} to {angle} degrees (pulse width: {pulse_width} μs)")

try:
    while True:
        angle = float(input("Enter the desired angle (-90 to 90 degrees): "))
        set_servo_angle(SERVO1_PIN, angle)
        # Uncomment the next line to control the second servo as well
        # set_servo_angle(SERVO2_PIN, angle)
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # Stop all servos and clean up
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()