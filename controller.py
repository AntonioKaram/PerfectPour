from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep
from threading import Thread

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

# Use Raspberry Pi v4 PWM pins
servo1 = Servo(12, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

def move_servo_smoothly(servo, start_position, end_position, duration):
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

def move_servos():
    # Create threads for both servo movements
    thread1 = Thread(target=move_servo_smoothly, args=(servo1, 1, 0, 2))
    thread2 = Thread(target=move_servo_smoothly, args=(servo2, 0, 1, 2))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    
    

try:
    for i in range(2):
        print("Moving both servos")
        thread1 = Thread(target=move_servo_smoothly, args=(servo1, 0, 1, 2))
        thread2 = Thread(target=move_servo_smoothly, args=(servo2, 1, 0, 2))
        
        # Start both threads
        thread1.start()
        thread2.start()
        
        # Wait for both threads to finish
        thread1.join()
        thread2.join()
        
        sleep(1)
        
    sleep(3) 
    move_servos()
        
        

except KeyboardInterrupt:
    print("Program stopped")
