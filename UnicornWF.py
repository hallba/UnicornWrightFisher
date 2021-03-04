#!/usr/bin/env python
"""Wright Fisher visualisation.

Visualises the growth of clones on a unicorn hathd.
"""
from time import sleep

import WrightFisher

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
        # each colour must be a key to an RGB value
        for i in range(self.totalColours):
            assert i in self.colourMap.keys()

    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to RGB."""
        self.colourMap = {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255)}

    def project(self):
        """Take the grid colours and visualise them on the matrix."""
        for i in range(self.size):
            for j in range(self.size):
                index = i + j * self.size
                colour = self.colourMap[self.colour[index]]
                unicorn.set_pixel(i, j, colour[0], colour[1], colour[2])
        unicorn.show()

    def runAndProject(self):
        """Run simulations indefinitely, projecting to the matrix."""
        while True:
            self.update()
            self.project()
            sleep(self.wait)


class CMYKUnicorn(UnicornSimulator):
    def pickColours(self):
        """Create colourMap dict, mapping 'colours' to CMYK."""
        self.colourMap = {0: (0, 0, 0), 1: (0, 255, 255), 2: (255, 0, 255), 3: (225, 225, 0)}


class GreyScaleUnicorn(UnicornSimulator):
    def pickColours(self):
        """Create colourMap dict with different shades of grey"""
        step = 255//self.totalColours
        self.colourMap = {k:(step*k, step*k, step*k) for k in range(self.totalColours)}

if __name__ == "__main__":
    grid = GreyScaleUnicorn(16, 10, 0.1, numberColours=50)
    grid.runAndProject()
