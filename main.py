"""Wright Fisher simulator.

Simulates the growth of clones in a 2D space.
"""
from time import sleep

import UnicornWF
#print('Unicorn size',w,'by',h)
#uni.set_pixel(x,y, r, g, b)

class GameClone(UnicornWF.UnicornSimulator):
    """Simulator for 2D Wright Fisher.

    Simulates and visualises a 2D square.
    """
    def runAndProject(self):
        """Run simulations indefinitely, projecting to the matrix."""
        # No mutations in interactive mode
        self.mutationRate=0
        while True:
            if UnicornWF.unicorn.is_pressed(UnicornWF.unicorn.BUTTON_A):
                self.mutate(colour=0)
                print("A")
            if UnicornWF.unicorn.is_pressed(UnicornWF.unicorn.BUTTON_B):
                self.mutate(colour=1)
                print("B")
            if UnicornWF.unicorn.is_pressed(UnicornWF.unicorn.BUTTON_X):
                self.mutate(colour=2)
                print("X")
            if UnicornWF.unicorn.is_pressed(UnicornWF.unicorn.BUTTON_Y):
                self.mutate(colour=3) 
                print("Y")
            self.update()
            self.project()
            sleep(self.wait)


if __name__=="__main__":
    print(UnicornWF.width,UnicornWF.height)
    grid = GameClone(UnicornWF.width*2,0,0.1,height=UnicornWF.height*2)
    grid.runAndProject()
