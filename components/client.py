from time import sleep
import requests
# from config.config import url
import OPi.GPIO as GPIO # a
from evdev import InputDevice, categorize, ecodes
import sys

url = "http://192.168.1.168:5000"
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# define device path
dev_path = "/dev/input/event0"

# Scancode: ASCIICode
scancodes = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 74: u'-', 100: u'RALT'
}

# define LED pins
redLED = 3
greenLED = 5
blueLED = 19

# set LED pins as output pins
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)


# turn on LED on
def LED_on(LED_pin):
    GPIO.output(LED_pin, GPIO.HIGH)


# turn LED off
def LED_off(LED_pin):
    GPIO.output(LED_pin, GPIO.LOW)


# turn on red LED  when waiting for input
def redLED_on():
    LED_on(redLED)
    LED_off(greenLED)
    LED_off(blueLED)


# turn on blue LED after receiving input
def blueLED_on():
    LED_off(redLED)
    LED_off(greenLED)
    LED_on(blueLED)


# turn on green LED after processing
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


def read_barcode():  # this functions reads the barcode
    read_barcode.dev = InputDevice(dev_path)
    read_barcode.dev.grab()
    barcode = ""
    for event in read_barcode.dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate == 1 and data.scancode != 42:  # Down events only and ignore shift presses
                key_lookup = scancodes.get(data.scancode) or u"UNKNOWN"
                if data.scancode != 28:  # data.scancode 28 is the Enter character
                    barcode += key_lookup
                else:
                    return barcode


def send_barcode(barcode):  # post barcode to url
    my_data = {"ID": barcode}
    response = requests.post(url, data=my_data["ID"])
    if response.text == "ok":  # waiting for feedback from server
        greenLED_on()
        sleep(1)
    else:
        print("Problem occured while sending barcode")


if __name__ == "__main__":
    setup()
    while True:
        redLED_on()
        print("Scan Barcode")
        try:
            code = read_barcode()
            print(code)
            blueLED_on()
            send_barcode(code)
            print("barcode sent")

        except FileNotFoundError:
            print("No devices found, please connect the barcode scanner")
        except OSError:
            print("Device disconnected")

        except KeyboardInterrupt:
            print(" Terminated")
            read_barcode.dev.ungrab()
            sys.exit(0)