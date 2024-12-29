from time import sleep, time
import requests
from config import url, department
import OPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes
import sys
import subprocess
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#define device path
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

#define LED pins
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

#turn on red LED when waiting for input
def redLED_on():
    LED_on(redLED)
    LED_off(greenLED)
    LED_off(blueLED)

#turn on blue LED after receiving input
def blueLED_on():
    LED_off(redLED)
    LED_off(greenLED)
    LED_on(blueLED)
    sleep(1.5)  # Sleep for 1.5 seconds

#turn on green LED after processing
def greenLED_on():
    LED_off(redLED)
    LED_off(blueLED)
    for _ in range(2):
        LED_on(greenLED)
        sleep(0.2)  # Blink green LED 
        LED_off(greenLED)
        sleep(0.2)

#turn on error LED on error
def errorLED_on():
    LED_off(greenLED)
    LED_off(blueLED)
    for _ in range(2):
        LED_on(redLED)
        sleep(0.2)  # Blink red
        LED_off(redLED)
        sleep(0.2)

def setup():
    LED_on(redLED)
    LED_on(greenLED)
    LED_on(blueLED)
    sleep(0.1)  # Sleep for 100 milliseconds
    LED_off(redLED)
    LED_off(greenLED)
    LED_off(blueLED)

def read_barcode(dev): #this functions reads the barcode
    barcode = ""
    shift_pressed = False
    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1:  # Down events only
                    if data.scancode == 42:  # LSHFT
                        shift_pressed = True
                    elif data.scancode == 28:  # Enter key
                        return barcode
                    else:
                        key_lookup = scancodes.get(data.scancode) or u"UNKNOWN"
                        if shift_pressed and key_lookup.isalpha():
                            key_lookup = key_lookup.upper()
                        barcode += key_lookup
                elif data.keystate == 0:  # Key release event
                    if data.scancode == 42:  # LSHFT
                        shift_pressed = False
    except OSError as e:
        print(f"Device disconnected during barcode read: {e}")
        raise

def send_barcode(barcode): #post barcode to url
    start_time = time()
    while True:
        try:
            response = requests.post(url, json={"ID": barcode, "Department": department}, timeout=10)
            if response.text == "ok": #waiting for feedback from server
                greenLED_on()
                break
            else:
                print("Problem occurred while sending barcode")
                errorLED_on()
                break
        except requests.exceptions.RequestException as e:
            if time() - start_time >= 10:
                print("Timeout or error occurred while sending barcode")
                errorLED_on()
                break

def get_device():
    try:
        dev = InputDevice(dev_path)
        dev.grab()
        print(f"Device found: {dev}")
        return dev
    except FileNotFoundError as e:
        print(f"No devices found, please connect the barcode scanner: {e}")
        errorLED_on()
    except OSError as e:
        print(f"Error accessing device: {e}")
        errorLED_on()
    return None

def kill_process_using_device(device_path):
    try:
        # Use lsof to find the process using the device
        result = subprocess.run(['lsof', device_path], capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.splitlines()
            if len(lines) > 1:  # First line is header
                for line in lines[1:]:
                    parts = line.split()
                    pid = int(parts[1])
                    print(f"Killing process {pid} using device {device_path}")
                    os.kill(pid, 9)
    except Exception as e:
        print(f"Error killing process: {e}")

if __name__ == "__main__":
    setup()
    kill_process_using_device(dev_path)  # Kill any process using the device
    dev = get_device()
    while True:
        try:
            if dev:
                redLED_on()
                print("Scan Barcode")
                try:
                    code = read_barcode(dev)
                    print(code)
                    blueLED_on()
                    send_barcode(code)
                    print("Barcode sent")
                except OSError as e:
                    print(f"Device disconnected: {e}")
                    errorLED_on()
                    dev = None  # Reset device to try reconnecting
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    errorLED_on()
            else:
                dev = get_device()
        except KeyboardInterrupt:
            print("Terminated")
            if dev:
                try:
                    dev.ungrab()
                except OSError as e:
                    print(f"Error ungrabbing device: {e}")
            sys.exit(0)