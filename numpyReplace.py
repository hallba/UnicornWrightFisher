"""Substitute for numpy.

A set of functions that (partially) replicate numpy 
functions so that code can run on pico.
"""

import random as rnd

print("Using pure python alternatives to numpy")

def zeros(number, dtype=float):
    if dtype == int:
        return([0 for _ in range(number)])
    elif dtype == float:
        return([0. for _ in range(number)])
    else:
        pass

class rng():
    def randint(self, lower, upper):
        # numpy does not include the upper bound, random does
        return(rnd.randint(lower, (upper-1)))
    def random(self):
        return(rnd.random())
    def normal(self, loc=0, scale=1):
        # not like for like. Revisit
        return(rnd.uniform((loc-scale*3/2), (loc+scale*3/2)))

random = rng()

def copy(someArray):
    return([item for item in someArray])
