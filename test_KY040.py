from ky040.KY040 import KY040
from RPi import GPIO
from time import sleep

def rotaryChange(direction):
    print("turned - " + str(direction))

# Callback for switch button pressed
def switchPressed():
    print("button pressed")

GPIO.setmode(GPIO.BOARD)

# Define your pins
CLOCKPIN = 15
DATAPIN = 16
SWITCHPIN = 18
ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChange, switchPressed)
ky040.start()

while True:
    sleep(1)