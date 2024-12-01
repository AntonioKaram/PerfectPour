from time import sleep
from threading import Thread
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

def set_servo_angle(servo_pin, angle):
    # Map angle (-90 to 90) to pulse width
    pulsewidth = ((angle + 90) * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 180) + MIN_PULSE_WIDTH
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

def main():
    try:
        while True:
            angle_input = input("Enter servo angle (-90 to 90 degrees) or 'exit' to quit: ")
            if angle_input.lower() == 'exit':
                break
            angle = float(angle_input)
            if -90 <= angle <= 90:
                set_servo_angle(SERVO1_PIN, angle)
                set_servo_angle(SERVO2_PIN, angle)
            else:
                print("Please enter an angle between -90 and 90 degrees.")
    except KeyboardInterrupt:
        pass
    finally:
        pi.set_servo_pulsewidth(SERVO1_PIN, 0)
        pi.set_servo_pulsewidth(SERVO2_PIN, 0)
        pi.stop()

if __name__ == "__main__":
    main()