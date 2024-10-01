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

def reset_servo(servo):
    servo.value = 1
    sleep(1) 
    servo.value = -1
    
    
try:
    while True:
        print("Resetting all servos")

        thread1 = Thread(target=reset_servo, args=(servo1))
        thread2 = Thread(target=reset_servo, args=(servo2))
        
        # Start both threads
        thread1.start()
        thread2.start()
        
        # Wait for both threads to finish
        thread1.join()
        thread2.join()

except KeyboardInterrupt:
    print("Program stopped")
