from time import sleep
import requests

import OPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes, list_devices
import signal, sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Url
url = ""

#define device path
dev_path ="/dev/input/event0"

# Scancode: ASCIICode
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 74: u'-', 100: u'RALT'
}

#define LED pins
redLED = 3
greenLED = 5
blueLED = 19

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

def setup(): #switches on all LEDs and Switches the off again
	LED_on(redLED)
	LED_on(greenLED)
	LED_on(blueLED)
	sleep(1)
	LED_off(redLED)
	LED_off(greenLED)
	LED_off(blueLED)

def signal_handler(signal, frame):
    print('Stopping')
    dev.ungrab()
    sys.exit(0)

if __name__ == "__main__":
    setup()
    while True:            
        try:
            redLED_on()
            dev = InputDevice(dev_path)
            signal.signal(signal.SIGINT, signal_handler)
            dev.grab()
            barcode = ""
            shift = False
            print("Scan Barcode")
            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY:
                    data = categorize(event)
                    if data.keystate == 1: #check key down events only
                        key_lookup = scancodes.get(data.scancode) or u"UNKNOWN{}".format(data.scancode)
                        if data.scancode == 42: 
                            blueLED_on()
                            print(barcode)
                            my_data = {"ID" : barcode}
                            response = requests.post(url, data = my_data["ID"]) #post data to Specified URL
                            barcode = ""
                            if response.text == "ok":
                                greenLED_on()
                                sleep(1)
                                break
                        else:
                            barcode += key_lookup
#Error Handling
            except KeyboardInterrupt:
                print("keyboard Interrupt")
                dev.close
            except FileNotFoundError:
                print("No devices found, please connect the scanner")

            except OSError:
                print("Device disconnected")
