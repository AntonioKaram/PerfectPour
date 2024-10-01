from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep
from threading import Thread

# Create a PiGPIOFactory instance
factory = PiGPIOFactory()

# Adjust min and max pulse width for your specific servos
min_pulse_width = 0.00008  # 0 degrees
max_pulse_width = 0.0023  # 180 degrees

# Use hardware PWM pins for two servos (e.g., GPIO 18 and GPIO 23)
servo1 = Servo(12, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)
servo2 = Servo(13, pin_factory=factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

def move_servo_smoothly(servo, start_position, end_position, duration):
    steps = 100  # Number of steps to take
    step_delay = duration / steps  # Time per step
    step_size = (end_position - start_position) / steps  # Increment for each step
    
    for i in range(steps + 1):
        position = start_position + i * step_size
        if position < 0:
            servo.min()  # Move to min if position is less than 0
        elif position > 1:
            servo.max()  # Move to max if position is greater than 1
        else:
            servo.value = position  # Set the servo to the interpolated position
        sleep(step_delay)

def move_servos():
    print("Moving both servos from min to max")
    # Create threads for both servo movements
    thread1 = Thread(target=move_servo_smoothly, args=(servo1, 0, 1, 2))  # Servo 1 from 0 to 1 over 2 seconds
    thread2 = Thread(target=move_servo_smoothly, args=(servo2, 0, 1, 2))  # Servo 2 from 0 to 1 over 2 seconds
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish
    thread1.join()
    thread2.join()

try:
    while True:
        move_servos()  # Move both servos
        sleep(1)  # Pause for 1 second before the next movement
        print("Moving both servos from max to min")
        # Move both servos back to minimum
        thread1 = Thread(target=move_servo_smoothly, args=(servo1, 1, 0, 2))  # Servo 1 from 1 to 0 over 2 seconds
        thread2 = Thread(target=move_servo_smoothly, args=(servo2, 1, 0, 2))  # Servo 2 from 1 to 0 over 2 seconds
        
        # Start both threads
        thread1.start()
        thread2.start()
        
        # Wait for both threads to finish
        thread1.join()
        thread2.join()

except KeyboardInterrupt:
    print("Program stopped")
