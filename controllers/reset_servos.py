
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

low = 22
high = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(low, GPIO.OUT)
GPIO.setup(high, GPIO.OUT)

print("setup...")
GPIO.output(low, GPIO.LOW)
GPIO.output(high, GPIO.LOW)
sleep(2)

i = 0
print("step 1..")


def move(low, high, duration):
    print("moving...")
    for i in range(duration * 10000000):
        GPIO.output(low, GPIO.LOW)
        GPIO.output(high, GPIO.HIGH)
    
# 3 for small
move(low, high, 5)
move(high, low, 5)
move(low, high, 5)
move(high, low, 5)
GPIO.cleanup()