from time import sleep
import requests
import OPi.GPIO as GPIO
from Config import Url
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

url = Url
#define LED pins
redLED, blueLED, greenLED =  3, 19, 5

#define system states: state 1 = waiting state, state 2 = processing state, state 3 = success feeback state
state = 1

#set LED pins as output pins
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)

#turn on LED on
def LED_on(LED_pin):
	GPIO.output(LED_pin, GPIO.HIGH)

#turn LED off
def LED_off(LED_pin):
        GPIO.output(LED_pin, GPIO.LOW)

#turn on red LED  when waiting for input
def redLED_on():
	LED_on(redLED)
	LED_off(greenLED)
	LED_off(blueLED)

#turn on blue LED after receiving input
def blueLED_on():
	LED_off(redLED)
	LED_off(greenLED)
	LED_on(blueLED)

#turn on green LED after processing
def greenLED_on():
	LED_off(redLED)
	LED_on(greenLED)
	LED_off(blueLED)

def setup():
	LED_on(redLED)
	LED_on(greenLED)
	LED_on(blueLED)
	sleep(1)
	LED_off(redLED)
	LED_off(greenLED)
	LED_off(blueLED)

if __name__ =="__main__":
	setup()
	state = 1
	while True:
		if (state == 1):#waiting for barcode
			redLED_on()
			barcode = input("Enter barcode:")
			if len(barcode) != 0:
				state = 2
		elif (state == 2):#processing state
			blueLED_on()
			my_data= {"ID":barcode}
			response = requests.post(url, data = my_data["ID"])
			if(response.text) == "ok":
				state=3
		elif(state==3):#success state
			greenLED_on()
			sleep(1)
			state = 1
			


