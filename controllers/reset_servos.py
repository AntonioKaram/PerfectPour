
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
sleep(5)

print("try1...")
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.HIGH)
sleep(5)

print("try2...")
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.LOW)
sleep(5)
