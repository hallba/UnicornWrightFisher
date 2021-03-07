#!/usr/bin/env python
"""Wright Fisher simulator.

Simulates the growth of clones in a 2D space.
"""

from time import sleep

import numpy as np

class Simulator:
    """Simulator for 2D Wright Fisher.

    Simulates and visualises a 2D square.
    """

    def __init__(self, size, mutationRate=0, wait=1, numberColours=4, height=None, advantage=0, special=None):
        """Initialise."""
        # Generate a grid of black cells initially
        self.width = size
        if height == None:
            self.height = size
        else:
            self.height = height
        self.population = self.width * self.height
        self.fitness = np.zeros(self.population)
        self.colour = np.zeros(self.population, dtype=int)

        self.nextFitness = np.zeros(self.population)
        self.nextColour = np.zeros(self.population, dtype=int)

        self.mutationRate = mutationRate
        self.timer = 0
        self.advantage = advantage

        self.mutantColour = 1
        self.totalColours = numberColours

        self.wait = wait

        self.special = special # parameters that can be specialised
        self.specificInit()
        """
                1
            4   0   2
                3
        """
    def specificInit(self):
        pass
    def up(self, currentPosition):
        """Return array index of space above currentPosition."""
        if currentPosition < self.width:
            return currentPosition + self.width * (self.height - 1)
        else:
            return currentPosition - self.width

    def down(self, currentPosition):
        """Return array index of space below currentPosition."""
        if currentPosition >= (self.width * (self.height - 1)):
            return currentPosition + self.width - self.population # got to check
        else:
            return currentPosition + self.width

    def right(self, currentPosition):
        """Return array index of space to right of currentPosition."""
        if (currentPosition + 1) % self.width == 0:
            return currentPosition - self.width + 1
        else:
            return currentPosition + 1

    def left(self, currentPosition):
        """Return array index of space to left of currentPosition."""
        if currentPosition % self.width == 0:
            return currentPosition + self.width - 1
        else:
            return currentPosition - 1

    def replacement(self, source, target):
        """Decide whether to replace cell and do it."""
        probability = 0.5 - self.fitness[target] + self.fitness[source]
        if np.random.random() < probability:
            # replaced by upper cell
            self.nextFitness[target] = self.fitness[source]
            self.nextColour[target] = self.colour[source]
        else:
            self.nextColour[target] = self.colour[target]
            self.nextFitness[target] = self.fitness[target]

    def tryReplaceNeighbour(self, currentPosition):
        """Pick a neighbour to try replace a cell and run replacement."""
        which = np.random.randint(0, 6)
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

    def colourUpdate(self):
        """Change the colour to the next colour, wrapping if appropriate."""
        self.mutantColour = (self.mutantColour + 1) % self.totalColours

    def mutate(self, colour=None):
        """Select a random cell and change fitness and colour."""
        cell = np.random.randint(0, self.population)
        self.fitness[cell] += np.random.normal(loc=self.advantage, scale=0.1)
        if colour == None:
            self.colour[cell] = self.mutantColour
        else:
            self.colour[cell] = colour
        self.colourUpdate()

    def update(self):
        """Update entire population."""
        for cellIndex in range(self.population):
            self.tryReplaceNeighbour(cellIndex)
        self.fitness = np.copy(self.nextFitness)
        self.colour = np.copy(self.nextColour)
        mutating = self.mutationRate and self.timer
        if mutating and self.timer % self.mutationRate == 0:
            self.mutate()
        self.timer += 1

    def printColours(self):
        """Print colours to screen."""
        for i in range(self.height):
            for j in range(self.width):
                print(self.colour[i + j * self.height], end="")
            print("")

    def runAndPrint(self, steps):
        """Update for several steps, printing at each step."""
        for _ in range(steps):
            self.update()
            self.printColours()
            print("=" * self.width)
            sleep(self.wait)
