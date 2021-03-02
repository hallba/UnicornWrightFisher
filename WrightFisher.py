import numpy as np
from time import sleep

colourMap = {   0: (0, 0, 0), 
                1: (255, 0, 0),
                2: (0, 255, 0),
                3: (0, 0, 255) }

class Simulator():
    def __init__(self,size,mutationRate=0,wait=1):
        # Generate a grid of black cells initially
        self.size = size
        self.population = size*size
        self.fitness = np.zeros(self.population)
        self.colour = np.zeros(self.population,dtype=int)

        self.nextFitness = np.zeros(self.population)
        self.nextColour = np.zeros(self.population,dtype=int)

        self.mutationRate = mutationRate
        self.timer = 0

        self.mutantColour = 1
        self.totalColours = len(colourMap.keys())

        self.wait = wait

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
        if currentPosition >= (self.size*(self.size-1)):
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
            self.nextFitness[target] = self.fitness[source]
            self.nextColour[target] = self.colour[source]
        else:
            self.nextColour[target] = self.colour[target]
            self.nextFitness[target] = self.fitness[target]
    def tryReplaceNeighbour(self, currentPosition):
        which = np.random.randint(0,6)
        if which == 0:
            # Do nothing as the cell is the same
            self.nextColour[currentPosition] = self.colour[currentPosition]
            self.nextFitness[currentPosition] = self.fitness[currentPosition]
        elif which == 1:
            self.replacement(self.up(currentPosition), currentPosition)
        elif which == 2:
            self.replacement(self.right(currentPosition), currentPosition)
        elif which == 3:
            self.replacement(self.down(currentPosition), currentPosition)
        else:
            self.replacement(self.left(currentPosition), currentPosition)
    def mutate(self):
        cell = np.random.randint(0,self.population)
        self.fitness[cell] += np.random.normal(loc=0.,scale=0.1)
        self.colour[cell] = self.mutantColour
        self.mutantColour = (self.mutantColour+1)%self.totalColours
    def update(self):
        for cellIndex in range(self.population):
            self.tryReplaceNeighbour(cellIndex)
        self.fitness = np.copy(self.nextFitness)
        self.colour = np.copy(self.nextColour)
        if self.mutationRate and self.timer and self.timer % self.mutationRate == 0:
            self.mutate()
        self.timer += 1
    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.colour[i+j*self.size], end='')
            print("")
    def runAndPrint(self,steps):
        for _ in range(steps):
            self.update()
            self.print()
            print("="*self.size)
            sleep(self.wait)