
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

low = 17
high = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(low, GPIO.OUT)
GPIO.setup(high, GPIO.OUT)

print("setup..")
GPIO.output(low, GPIO.LOW)
GPIO.output(high, GPIO.LOW)
sleep(2)

i = 0
print("step 1..")


def move(low, high):
    print("backwards...")
    for i in range(30000000):
        GPIO.output(low, GPIO.LOW)
        GPIO.output(high, GPIO.HIGH)
    

move(low, high)
move(high, low)
move(low, high)
move(high, low)
GPIO.cleanup()