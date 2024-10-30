from time import sleep
from math import sin, radians
from gpiozero import Servo
from threading import Thread
from gpiozero.pins.pigpio import PiGPIOFactory

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

# Use Raspberry Pi v4 PWM pins
servo1 = Servo(12, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

top_linear = Servo(17, pin_factory=factory)
bottom_linear = Servo(27, pin_factory=factory)

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
  
def pierce_can():
    print("Piercing the can...")
    top_linear.max()
    sleep(2)
    print("Retracting piercing servo...")
    top_linear.min()
    print("Done piercing...\n")
    sleep(1)
    
def setup_cup():
    print("Moving cup to initial position...")
    bottom_linear.max()
    print("Done moving cup...\n")
    sleep(1)
    
def tilt_cup():
    bottom_linear.value = 0.8
    sleep(2)
    bottom_linear.min()
    sleep(1)
    
def pour():
    print("Pouring...")
    thread1 = Thread(target=rotate_servo, args=(servo1, 0, 0.8, 2))
    thread2 = Thread(target=rotate_servo, args=(servo2, 1, 0.2, 2))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    sleep(1)
    
def main():
    
    ## Phase 1 - Pierce can and set up cup
    print("---------------------------------------------------------------")
    print("Starting Phase 1")
    thread1 = Thread(target=pierce_can)
    thread2 = Thread(target=setup_cup)
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    print("Phase 1 complted...")
    print("---------------------------------------------------------------\n\n")
    
    
    ## Phase 2 - Pour can and tilt cup
    print("---------------------------------------------------------------")
    print("Starting Phase 2")
    thread1 = Thread(target=pour)
    thread2 = Thread(target=tilt_cup)
    
    # Start both threads
    thread1.start()
    thread2.start
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    print("Phase 2 complted...")
    print("---------------------------------------------------------------\n\n")
  
try:
    main()
       
except KeyboardInterrupt:
    print("Program stopped")
