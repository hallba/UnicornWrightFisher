#!/usr/bin/env python
"""Wright Fisher visualisation.

Visualises the growth of clones on a unicorn hathd.
"""
from time import sleep

import cv2

import WrightFisher

import numpy as np

try:
    import unicornhathd as unicorn
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width, height = unicorn.get_shape()


class UnicornSimulator(WrightFisher.Simulator):
    """Simulator for 2D Wright Fisher.

    Simulates and visualises a 2D square in an LED matrix.
    """

    def specificInit(self):
        """We need a map between 'colours' and RGB values for display."""
        self.pickColours()
        assert self.totalColours == len(self.colourMap.keys())
        # each colour must be a key to an RGB value
        for i in range(self.totalColours):
            assert i in self.colourMap.keys()

    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to RGB."""
        if self.special == None or "colourMap" not in self.special:
            self.colourMap = {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255)}
        else:
            self.colourMap = self.special["colourMap"]

    def project(self):
        """Take the grid colours and visualise them on the matrix."""
        if self.size == 16:
            # no scaling necessary
            for i in range(self.size):
                for j in range(self.size):
                    index = i + j * self.size
                    colour = self.colourMap[self.colour[index]]
                    unicorn.set_pixel(i, j, colour[0], colour[1], colour[2])
            unicorn.show()
        else:
            def colourConvert(index):
                """Convert an index into its colour."""
                return(self.colourMap[self.colour[index]])
            cMat = [[colourConvert(x + y * self.size) for y in range(self.size)] for x in range(self.size)]
            img = np.array(cMat, dtype=float)
            res = cv2.resize(img, dsize=(16, 16))
            for i in range(16):
                for j in range(16):
                    index = i + j * self.size
                    unicorn.set_pixel(i, j, res[i, j, 0], res[i, j, 1], res[i, j, 2])
            unicorn.show()

    def runAndProject(self):
        """Run simulations indefinitely, projecting to the matrix."""
        while True:
            self.update()
            self.project()
            sleep(self.wait)


class CMYKUnicorn(UnicornSimulator):
    """Unicorn Simulator that displays CMYK instead of RBG+Black."""
    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to CMYK."""
        self.colourMap = {0: (0, 0, 0), 1: (0, 255, 255), 2: (255, 0, 255), 3: (225, 225, 0)}


class GreyScaleUnicorn(UnicornSimulator):
    """Unicorn Simulator that displays greyscale instead of RBG+Black."""
    def pickColours(self):
        """Create colourMap dict with different shades of grey"""
        step = 255//self.totalColours
        self.colourMap = {k:(step*k, step*k, step*k) for k in range(self.totalColours)}
    def colourUpdate(self):
        """Change the colour to the next colour, switch to count down if appropriate."""
        if not hasattr(self, 'goingDown'):
            if self.mutantColour == self.totalColours - 1:
                self.goingDown = True
                self.mutantColour -= 1
            else:
                self.mutantColour += 1
        else:
            if self.goingDown and self.mutantColour > 0:
                self.mutantColour -= 1
            elif self.mutantColour == 0:
                self.goingDown = False
                self.mutantColour +=1
            elif self.mutantColour == self.totalColours - 1:
                self.goingDown = True
                self.mutantColour -= 1
            else:
                self.mutantColour += 1

if __name__ == "__main__":
    grid = UnicornSimulator(16, 10, 0.1)
    grid.runAndProject()
