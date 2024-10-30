
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

in1 = 17
in2 = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

print("setup..")
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
sleep(2)

i = 0
print("step 1..")


def backward():
    print("backwards...")
    for i in range(30000000):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        

def forward():
    print("forward...")        
    for i in range(30000000):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    

forward()
backward()
forward()
backward()
GPIO.cleanup()