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
servo1 = Servo(12, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# Set up linear servos
bottom_low = 22
bottom_high = 23

top_low = 17
top_high = 27

MAX_BOTTOM = 10
MAX_TOP = 5

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
    servo.min() if start else servo.max()


def top():
    pass

def bottom():
    pass

def rot():
    rotate_servo_smooth(servo1, 0, 90, 0.01)
    
def reset():
    reset_servo(servo1)
    reset_servo(servo2)
    
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