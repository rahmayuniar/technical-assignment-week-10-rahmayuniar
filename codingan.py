import RPi.GPIO as GPIO
import time
import requests

ldr_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(ldr_pin, GPIO.IN)

TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"  # Put your TOKEN here
DEVICE_LABEL = "import_data"  # Put your device label here 
VARIABLE_LABEL_1 = "cahaya"  # Put your first variable label here

def build_payload(variable_1):
    # Wait for the LDR to stabilize
    time.sleep(1)
    ldr = GPIO.input(ldr_pin)
    # Read the LDR value

    payload = {variable_1: ldr
        }
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")
    print(payload) 


if _name_ == '_main_':
    while (True):
        main()
        time.sleep(1)