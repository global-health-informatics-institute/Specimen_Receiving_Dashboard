"""
This script is used to test the GPIO pins on the Raspberry Pi.
Specifically the LED pins.
Each LED pin is turned on for 5 seconds and then turned off. in a loop.
Should be ran durring the initial setup of the station and after configuring all requirements as venv and dependencies.
"""
#define LED pins
from time import sleep


redLED = 3
greenLED = 5
blueLED = 19

#set LED pins as output pins
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)

#turn on LED
def LED_on(LED_pin):
    GPIO.output(LED_pin, GPIO.HIGH)

#turn LED off
def LED_off(LED_pin):
    GPIO.output(LED_pin, GPIO.LOW)


def test_LED(LED_pin):
    LED_off(redLED)
    LED_off(blueLED)
    LED_off(greenLED)
    LED_on(LED_pin)
    sleep(5)

LED_array = [redLED, greenLED, blueLED] 

if __name__ == "__main__":
    while True:
        for led in LED_array:
            test_LED(led)