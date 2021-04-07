#!/usr/bin/env python
"""Clone wars simulator.

Simulates the growth of clones in a 2D space.
Mutations are induced by button presses.

Currently untested.
"""

import splash
splash.splashScreen("CloneWars!",rotation=270)

import signal                   
import sys
import RPi.GPIO as GPIO

try:
    import numpy as np
except ImportError:
    import numpyReplace as np

from UnicornWF import UnicornSimulator

# Need to check the pin numbers
RED_BUTTON_GPIO = 21
BLUE_BUTTON_GPIO = 16
GREEN_BUTTON_GPIO = 12
BLACK_BUTTON_GPIO = 25

GPIO.setmode(GPIO.BCM)
buttons = [RED_BUTTON_GPIO, BLUE_BUTTON_GPIO, GREEN_BUTTON_GPIO, BLACK_BUTTON_GPIO]

class DecayMutation(UnicornSimulator):
    """Random mutation turns cells black"""
    def mutate(self, colour=0):
        """Select a random cell and change fitness and colour to black."""
        cell = np.random.randint(0, self.population)
        self.fitness[cell] += np.random.normal(loc=self.advantage, scale=0.1)
        if colour == None:
            self.colour[cell] = self.mutantColour
        else:
            self.colour[cell] = colour
        self.colourUpdate()

if __name__ == "__main__":
    for BUTTON_GPIO in buttons:
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    grid = DecayMutation(16, 30, 0.1, advantage=0.1)
    def redMutation(channel):
        print("red")
        grid.mutate(1)
    def blueMutation(channel):
        print("blue")
        grid.mutate(3)
    def greenMutation(channel):
        grid.mutate(2)
    def blackMutation(channel):
        grid.mutate(1)
    print("setup buttons")
    GPIO.add_event_detect(RED_BUTTON_GPIO, GPIO.FALLING, 
            callback=redMutation, bouncetime=50)
    GPIO.add_event_detect(BLUE_BUTTON_GPIO, GPIO.FALLING, 
            callback=blueMutation, bouncetime=50)
    GPIO.add_event_detect(GREEN_BUTTON_GPIO, GPIO.FALLING, 
            callback=greenMutation, bouncetime=50)
    GPIO.add_event_detect(BLACK_BUTTON_GPIO, GPIO.FALLING, 
            callback=blackMutation, bouncetime=50)
    print("enter loop")
    grid.runAndProject()

GPIO.cleanup()
