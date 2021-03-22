#!/usr/bin/env python
"""Wright Fisher visualisation.

Visualises the growth of clones on a unicorn hathd.
"""
from time import sleep

try:
    import cv2
    openCVAvailable = True
except ImportError:
    openCVAvailable = False
    import imageScale

import WrightFisher

try:
    import numpy as np
except ImportError:
    import numpyReplace as np

try:
    import unicornhathd as unicorn
    pico = False
    pi = True
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
    width, height = unicorn.get_shape()
    print("Running on unicornhathd")
except ImportError:
    try:
        import picounicorn as unicorn
        from machine import Pin
        unicorn.init()
        width = unicorn.get_width()
        height = unicorn.get_height()
        led = Pin(25, Pin.OUT)
        pico = True
        pi = False
        print("Running on pico")
    except ImportError:
        pico = False
        pi = False
        from unicorn_hat_sim import unicornhathd as unicorn
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        width, height = unicorn.get_shape()
        print("Running on simulator")

class UnicornSimulator(WrightFisher.Simulator):
    """Simulator for 2D Wright Fisher.

    Simulates and visualises a 2D square in an LED matrix.
    """

    def specificInit(self):
        """We need a map between 'colours' and RGB values for display."""
        self.pickColours()
        assert self.totalColours <= len(self.colourMap)

    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to RGB."""
        if self.special == None or "colourMap" not in self.special:
            self.colourMap = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        else:
            self.colourMap = self.special["colourMap"]

    def project(self):
        """Take the grid colours and visualise them on the matrix."""
        if self.height == height and self.width == width:
            # no scaling necessary
            for i in range(self.width):
                for j in range(self.height):
                    index = i + j * self.width
                    colour = self.colourMap[self.colour[index]]
                    unicorn.set_pixel(i, j, colour[0], colour[1], colour[2])
            if not pico:
                unicorn.show()
        else:
            def colourConvert(index):
                """Convert an index into its colour."""
                return(self.colourMap[self.colour[index]])
            if openCVAvailable:
                cMat = [[colourConvert(x + y * self.width) for y in range(self.height)] for x in range(self.width)]
                img = np.array(cMat, dtype=float)
                res = cv2.resize(img, dsize=(width, height))
                for i in range(width):
                    for j in range(height):
                        index = i + j * self.width
                        unicorn.set_pixel(i, j, res[i, j, 0], res[i, j, 1], res[i, j, 2])
                if not pico: 
                    unicorn.show()
            else:
                cMat = [[colourConvert(x + y * self.width) for y in range(self.height)] for x in range(self.width)]
                res = imageScale.downScaleImage(cMat,width,height)
                for i in range(width):
                    for j in range(height):
                        index = i + j * self.width
                        if pico:
                            r = int(res[i][j][0])
                            g = int(res[i][j][1])
                            b = int(res[i][j][2])
                        else:
                            r = res[i, j, 0]
                            g = res[i, j, 1]
                            b = res[i, j, 2]
                        unicorn.set_pixel(i, j, r, g, b)
                if not pico:
                    unicorn.show()

    def runAndProject(self):
        """Run simulations indefinitely, projecting to the matrix."""
        while True:
            self.update()
            self.project()
            if pico:
                led.toggle()
            sleep(self.wait)


class CMYKUnicorn(UnicornSimulator):
    """Unicorn Simulator that displays CMYK instead of RBG+Black."""
    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to CMYK."""
        self.colourMap = [(0, 0, 0), (0, 255, 255), (255, 0, 255),  (225, 225, 0)]


class GreyScaleUnicorn(UnicornSimulator):
    """Unicorn Simulator that displays greyscale instead of RBG+Black."""
    def pickColours(self):
        """Create colourMap dict with different shades of grey"""
        step = 255//self.totalColours
        self.colourMap = [(step*k, step*k, step*k) for k in range(self.totalColours)]
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
    grid = UnicornSimulator(width, 10, 0.1, height=height)
    grid.runAndProject()
