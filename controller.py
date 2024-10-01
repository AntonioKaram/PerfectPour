from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
from gpiozero import Servo
from time import sleep

Servo.pin_factory = PiGPIOFactory()
servo = Servo(25)

try:
    while True:
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
        
except KeyboardInterrupt:
	print("Program stopped")