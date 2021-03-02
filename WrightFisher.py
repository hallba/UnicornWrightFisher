import numpy as np

colourMap = {   0: (0, 0, 0), 
                1: (255, 0, 0),
                2: (0, 255, 0),
                3: (0, 0, 255) }

class Simulator():
    def __init__(self,size):
        # Generate a grid of black cells initially
        self.size = size
        self.population = size*size
        self.fitness = np.zeros(self.population)
        self.colour = np.zeros(self.population,dtype=int)
        self.fitness[3+3*self.size] = 1
        self.colour[3+3*self.size] = 1
        '''
                1
            4   0   2
                3
        '''
    def up(self, currentPosition):
        if currentPosition < self.size:
            return(currentPosition + self.size*(self.size-1))
        else:
            return(currentPosition - self.size)
    def down(self, currentPosition):
        if currentPosition > (self.size*(self.size-1)):
            return(currentPosition - self.size*(self.size-1))
        else:
            return(currentPosition + self.size)
    def right(self, currentPosition):
        if currentPosition % (self.size-1) == 0:
            return(currentPosition-self.size+1)
        else:
            return(currentPosition+1)
    def left(self, currentPosition):
        if currentPosition % self.size == 0:
            return(currentPosition+self.size-1)
        else:
            return(currentPosition-1)
    def replacement(self,source,target):
        if np.random.random() < (0.5 - self.fitness[target] + self.fitness[source]):
            # replaced by upper cell
            self.fitness[target] = self.fitness[source]
            self.colour[target] = self.fitness[source]
        else:
            pass
    def tryReplaceNeighbour(self, currentPosition):
        which = np.random.randint(0,6)
        if which == 0:
            # Do nothing as the cell is the same
            pass
        elif which == 1:
            self.replacement(self.up(currentPosition), currentPosition)
        elif which == 2:
            self.replacement(self.right(currentPosition), currentPosition)
        elif which == 3:
            self.replacement(self.down(currentPosition), currentPosition)
        else:
            self.replacement(self.left(currentPosition), currentPosition)
    def update(self):
        for cellIndex in range(self.population):
            self.tryReplaceNeighbour(cellIndex)
    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.colour[i+j*self.size], end='\t')
            print("")
    def runAndPrint(self,steps):
        for _ in range(steps):
            self.update()
            self.print()