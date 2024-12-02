from time import sleep
from math import sin, radians
from gpiozero import Servo
from threading import Thread
import RPi.GPIO as GPIO # type: ignore
from gpiozero.pins.pigpio import PiGPIOFactory

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

# Set up rotating servos
#servo1 = Servo(12, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

# Set up linear servos
GPIO.setup(bottom_low, GPIO.OUT)
GPIO.setup(bottom_high, GPIO.OUT)
GPIO.setup(top_low, GPIO.OUT)
GPIO.setup(top_high, GPIO.OUT)

GPIO.output(bottom_low, GPIO.LOW)
GPIO.output(bottom_high, GPIO.LOW)
GPIO.output(top_low, GPIO.LOW)
GPIO.output(top_high, GPIO.LOW)

def GPIO_move(in0, in1, duration):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    
    sleep(duration)
    
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)
    
def GPIO_stop(in0, in1):
    GPIO.output(in0, GPIO.LOW)
    GPIO.output(in1, GPIO.LOW)

def rotate_servo_smooth(servo, start_position, end_position, step):
    for i in range(start_position, end_position):
        servo.value = sin(radians(i))
        sleep(step)
        
def rotate_servo(servo, start_position, end_position, duration):
    steps = 500
    step_delay = duration / steps
    step_size = (end_position - start_position) / steps
    
    for i in range(steps + 1):
        position = start_position + i * step_size
        if position < 0:
            servo.min()
        elif position > 1:
            servo.max()
        else:
            servo.value = position
        sleep(step_delay)
        
def reset_servo(servo, start=True):
    servo.value = 0 if start else 1
  
def pierce_can():
    print("Piercing the can...")
    GPIO_move(top_low, top_high, MAX_TOP)
    
    print("Retracting piercing servo...")
    GPIO_move(top_high, top_low, MAX_TOP)
    
    print("Done piercing...\n")
    sleep(1)
    
def setup_cup():
    print("Moving cup to initial position...")
    GPIO_move(bottom_low, bottom_high, MAX_BOTTOM)
    
    print("Done moving cup...")
    sleep(1)
    
def tilt_cup():
    GPIO_move(bottom_high, bottom_low, MAX_BOTTOM * 0.2)
    
    sleep(3)
    GPIO_move(bottom_high, bottom_low, MAX_BOTTOM * 0.8)
    sleep(1)
    
def pour():
    sleep(MAX_BOTTOM*0.15)
    print("Pouring...")
    # thread1 = Thread(target=rotate_servo, args=(servo1, 0, 0.5, 0.1))
    rotate_servo(servo2, 0, 1, 0.1)
    
    # Start both threads
    # thread1.start()
    
    # Wait for both threads to finish
    # thread1.join()
    
    # thread1 = Thread(target=rotate_servo, args=(servo1, 0.5, 1, 1))
    
    # Start both threads
    # thread1.start()
    
    # Wait for both threads to finish
    # thread1.join()
    
    
    
    # Start both threads
    # thread1.start()
    
    # Wait for both threads to finish
    # thread1.join()
    
def main():
    print("\n\n---------------------------------------------------------------")
    print("Starting Setup")
    print("Aligning Cup...")
    # # thread1 = Thread(target=reset_servo, args=(servo1))
    # thread2 = Thread(target=reset_servo, args=(servo2))
    
    # # Start both threads
    # # thread1.start()
    # thread2.start()
    
    # # Wait for both threads to finish
    # # thread1.join()
    # thread2.join()
    
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
  
try:
    main()
       
except KeyboardInterrupt:
    print("Program stopped")
