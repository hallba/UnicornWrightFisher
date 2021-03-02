#!/usr/bin/env python
import unicornhathd as unicorn
import WrightFisher
from time import sleep

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

colourMap = {   0: (0, 0, 0), 
                1: (255, 0, 0),
                2: (0, 255, 0),
                3: (0, 0, 255) }

class UnicornSimulator(WrightFisher.Simulator):
    def project(self):
        for i in range(self.size):
            for j in range(self.size):
                index =i+j*self.size
                colour = colourMap[self.colour[index]]
                unicorn.set_pixel(i,j,colour[0],colour[1],colour[2])
        unicorn.show()
    def runAndProject(self,steps):
        for _ in range(steps):
            self.update()
            self.project()
            #self.print()
            sleep(self.wait)

if __name__ == "__main__":
    grid = UnicornSimulator(16,10,0.1)
    grid.runAndProject(100000)
