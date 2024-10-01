from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.native import NativeFactory
from gpiozero import Servo
from time import sleep

Servo.pin_factory = NativeFactory()
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