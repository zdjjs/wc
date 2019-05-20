#!/usr/bin/env python

import os
import sys
import time
import RPi.GPIO as GPIO
from slackclient import SlackClient

BCM = os.getenv('WC_BCM', 23)
TRY_TIME = 7
TURN = 300
SLACK_API_TOKEN = os.getenv('WC_API_TOKEN')
sc = SlackClient(SLACK_API_TOKEN)


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
    for i in range(TURN):
        print('TURN ' + str(i))
        out_counter = 0
        in_counter = 0
        for j in range(TRY_TIME):
            if GPIO.input(BCM) == GPIO.LOW:
                print('absence')
                out_counter += 1
            else:
                print('presence')
                in_counter += 1
            time.sleep(1)
            sc.rtm_read()

        if in_counter < out_counter:
            opened()
        else:
            closed()
    sys.exit()


if __name__ == "__main__":
    print('BCM              : ' + str(BCM))
    print('TRY_TIME         : ' + str(TRY_TIME))
    print('TURN             : ' + str(TURN))
    print('SLACK_API_TOKEN  : ' + str(SLACK_API_TOKEN))
    print('----- START -----')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BCM, GPIO.IN)
    if sc.rtm_connect(with_team_state=False, auto_reconnect=True):
        main()
