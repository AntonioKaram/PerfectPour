
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(True)

in1 = 17
in2 = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

print("setup..")
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
sleep(5)


while True:
    user_input = input()
    
    if user_input == "w":
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        
    else:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)

