import os
import time
import RPi.GPIO as GPIO
import slackclient

BCM = os.getenv('WC_BCM', 23)
EXTENSION_TIME = 5
SLACK_API_TOKEN = os.getenv('WC_API_TOKEN')
sc = slackclient(SLACK_API_TOKEN)


def closed():
    print('CLOSED')
    sc.api_call(
        "users.setPresence",
        presence="auto",
    )


def opened():
    print('OPENED')
    sc.api_call(
        "users.setPresence",
        presence="away",
    )


def main():
    out_counter = EXTENSION_TIME
    in_counter = EXTENSION_TIME
    while True:
        if GPIO.input(BCM) == GPIO.LOW:
            print('absence')
            out_counter -= 1
            in_counter = EXTENSION_TIME
            if out_counter <= 0:
                opened()
                out_counter = EXTENSION_TIME
        else:
            print('presence')
            out_counter = EXTENSION_TIME
            in_counter -= 1
            if in_counter <= 0:
                closed()
                in_counter = EXTENSION_TIME

        time.sleep(1)


if __name__ == "__main__":
    print('BCM                   : ' + str(BCM))
    print('EXTENSION_TIME        : ' + str(EXTENSION_TIME))
    print('SLACK_API_TOKEN       : ' + str(SLACK_API_TOKEN))
    print('----- START -----')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BCM, GPIO.IN)
    sc.rtm_connect()
    main()
