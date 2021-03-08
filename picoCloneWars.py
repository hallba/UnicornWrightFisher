"""Wright Fisher simulator.

Simulates the growth of clones in a 2D space.
"""
from time import sleep

import UnicornWF
#print('Unicorn size',w,'by',h)
#uni.set_pixel(x,y, r, g, b)

class PicoCornSimulator(UnicornWF.UnicornSimulator):
    """Simulator for 2D Wright Fisher.

    Simulates and visualises a 2D square.
    """

    pass

if __name__=="__main__":
    grid = PicoCornSimulator()
    grid.runAndPrint(100)

