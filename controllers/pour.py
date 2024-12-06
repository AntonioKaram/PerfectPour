from time import sleep
from math import sin, radians
from gpiozero import Servo
from threading import Thread
import RPi.GPIO as GPIO # type: ignore
from gpiozero.pins.pigpio import PiGPIOFactory
import pigpio

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon. Ensure `pigpiod` is running.")

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

MAX_BOTTOM = 27
MAX_TOP = 15

# Set up linear servos
bottom_low = 22
bottom_high = 23

top_low = 17
top_high = 27

backgate_low = 2
backgate_high = 3

frontgate_low = 4
frontgate_high = 14

# Set up linear servos
GPIO.setup(bottom_low, GPIO.OUT)
GPIO.setup(bottom_high, GPIO.OUT)
GPIO.setup(top_low, GPIO.OUT)
GPIO.setup(top_high, GPIO.OUT)
GPIO.setup(backgate_low, GPIO.OUT)
GPIO.setup(backgate_high, GPIO.OUT)
GPIO.setup(frontgate_low, GPIO.OUT)
GPIO.setup(frontgate_high, GPIO.OUT)

GPIO.output(bottom_low, GPIO.LOW)
GPIO.output(bottom_high, GPIO.LOW)
GPIO.output(top_low, GPIO.LOW)
GPIO.output(top_high, GPIO.LOW)
GPIO.output(backgate_low, GPIO.LOW)
GPIO.output(backgate_high, GPIO.LOW)
GPIO.output(frontgate_low, GPIO.LOW)
GPIO.output(frontgate_high, GPIO.LOW)

# GPIO Pins for the servos
SERVO1_PIN = 12
SERVO2_PIN = 13

# Calibration values from datasheet
SERVO_CALIBRATION = {
    'MIN': 500,    # Minimum pulse width in microseconds
    'MAX': 2500,   # Maximum pulse width in microseconds
    'CENTER': 1500 # Neutral (center) pulse width in microseconds
}

def calculate_pulse_width(position, calibration):
    """
    Calculate the pulse width for the given normalized position.
    - `position`: Normalized value (-1.0 to 1.0) for servo angle.
    """
    if position < -1.0 or position > 1.0:
        raise ValueError("Position must be between -1.0 and 1.0")
    
    if position <= 0:
        return int(calibration['CENTER'] + position * (calibration['CENTER'] - calibration['MIN']))
    else:
        return int(calibration['CENTER'] + position * (calibration['MAX'] - calibration['CENTER']))

def smooth_move_servo(pin, start_position, target_position, calibration, steps=50, delay=0.01):
    """
    Smoothly move a servo from start_position to target_position.
    - `start_position` and `target_position` are normalized (-1.0 to 1.0).
    """
    start_pulse = calculate_pulse_width(start_position, calibration)
    target_pulse = calculate_pulse_width(target_position, calibration)
    step_size = (target_pulse - start_pulse) / steps

    for step in range(steps + 1):
        pulse = start_pulse + step * step_size
        pi.set_servo_pulsewidth(pin, int(pulse))
        sleep(delay)

def GPIO_move(in0, in1, duration):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    
    sleep(duration)
    
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)
    
def GPIO_stop(in0, in1):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)

def pierce_can():
    print("Piercing the can...")
    GPIO_move(top_low, top_high, MAX_TOP)
    
    print("Retracting piercing servo...")
    GPIO_move(top_high, top_low, MAX_TOP)
    
    print("Done piercing...\n")
    sleep(1)
    
def setup_cup():
    print("Moving cup to initial position...")
    GPIO_move(bottom_low, bottom_high, MAX_BOTTOM*0.7)
    
    print("Done moving cup...")
    sleep(1)
    
def tilt_cup():
    GPIO_move(bottom_high, bottom_low, MAX_BOTTOM * 0.05)
    
    sleep(2)
    GPIO_move(bottom_high, bottom_low, MAX_BOTTOM * 0.65)
    sleep(1)
    
def pour():
    print("Pouring...")
    
    smooth_move_servo(SERVO1_PIN, -0.3, -1, SERVO_CALIBRATION, steps=100, delay=0.02)
    
    
def main():
    print("\n\n---------------------------------------------------------------")
    print("Starting Setup")
    print("Aligning Cup...")

    smooth_move_servo(SERVO1_PIN, -1, -1, SERVO_CALIBRATION)
    smooth_move_servo(SERVO1_PIN, -1, -0.3, SERVO_CALIBRATION)

    setup_cup()
    
    print("Setup complted...")
    print("---------------------------------------------------------------\n\n")
    
    # ## Phase 1 - Pierce can and set up cup
    # print("---------------------------------------------------------------")
    # print("Starting Phase 1")
    # thread1 = Thread(target=pierce_can)
    # thread2 = Thread(target=setup_cup)
    
    # # Start both threads
    # thread1.start()
    # thread2.start()
    
    # # Wait for both threads to finish
    # thread1.join()
    # thread2.join()
    
    # print("Phase 1 complted...")
    # print("---------------------------------------------------------------\n\n")
    
    
    ## Phase 2 - Pour can and tilt cup
    print("---------------------------------------------------------------")
    print("Starting Phase 2")
    thread1 = Thread(target=pour)
    thread2 = Thread(target=tilt_cup)
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    print("Phase 2 complted...")
    print("---------------------------------------------------------------\n\n")
        
    GPIO.cleanup()
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()

  
try:
    main()
       
except KeyboardInterrupt:
    print("Program stopped")
