#!/usr/bin/env python
"""Clone wars simulator.

Simulates the growth of clones in a 2D space.
Mutations are induced by button presses.

Currently untested.
"""

import signal                   
import sys
import RPi.GPIO as GPIO

from UnicornWF import UnicornSimulator

# Need to check the pin numbers
RED_BUTTON_GPIO = 11
BLUE_BUTTON_GPIO = 15
GREEN_BUTTON_GPIO = 29
BLACK_BUTTON_GPIO = 33

buttons = [RED_BUTTON_GPIO, BLUE_BUTTON_GPIO, GREEN_BUTTON_GPIO, BLACK_BUTTON_GPIO]

if __name__ == "__main__":
    for BUTTON_GPIO in buttons:
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    grid = UnicornSimulator(16, 0, 0.1, advantage=0.1)
    def redMutation(channel):
        grid.mutate(1)
    def blueMutation(channel):
        grid.mutate(2)
    def greenMutation(channel):
        grid.mutate(3)
    def blackMutation(channel):
        grid.mutate(1)
    GPIO.add_event_detect(RED_BUTTON_GPIO, GPIO.FALLING, 
            callback=redMutation, bouncetime=50)
    GPIO.add_event_detect(BLUE_BUTTON_GPIO, GPIO.FALLING, 
            callback=blueMutation, bouncetime=50)
    GPIO.add_event_detect(GREEN_BUTTON_GPIO, GPIO.FALLING, 
            callback=greenMutation, bouncetime=50)
    GPIO.add_event_detect(BLACK_BUTTON_GPIO, GPIO.FALLING, 
            callback=blackMutation, bouncetime=50)
    grid.runAndProject()