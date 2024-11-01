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

# Set up rotating servos
servo1 = Servo(12, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

# Set up linear servos
bottom_low = 22
bottom_high = 23

top_low = 17
top_high = 27

MAX_BOTTOM = 30
MAX_TOP = 15

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
    servo.min() if start else servo.max()


def top():
    pass

def bottom():
    pass

def rot():
    # print("Pouring...")
    # thread1 = Thread(target=rotate_servo, args=(servo1, 0, 1, 1))
    # thread2 = Thread(target=rotate_servo, args=(servo2, 1, 0, 1))
    
    # # Start both threads
    # thread1.start()
    # thread2.start()
    
    # # Wait for both threads to finish
    # thread1.join()
    # thread2.join()
    
    # sleep(1)
    
    # reset()
    
    while True:
        rotate_servo(servo1, 0, 1, 0.5)
        rotate_servo(servo2, 1, 0, 0.5)
        rotate_servo(servo1, 1, 0, 0.5)
        rotate_servo(servo2, 0, 1, 0.5)
    
def reset():
    reset_servo(servo1)
    reset_servo(servo2,False)
    
    
run = True
while run:
    print("----------------------------------------------")
    print("-----------------TEST MODULE------------------")
    print("----------------------------------------------")
    print("Options")
    print("1. top linear (t)")
    print("2. bottom linear (b)")
    print("3. Rotational (r)")
    print("4. Reset (reset)")
    print("5. Exit (q)")
    
    
    test = input("Which test do you want to run? ")
    
    
    match test:
        case "t":
            top()
        case "b":
            bottom()
        case "r":
            rot()
        case "reset":
            reset()
        case "q":
            run = False
            reset_servo(servo1)
            reset_servo(servo2, False)
            GPIO.cleanup()
        case _:
            pass