#!/usr/bin/env python
"""Image scaling library

Pure python image scaling
"""

def tripletAverage(sample):
    number = len(sample)
    average = [0, 0, 0]
    for colour in sample:
        for index, component in enumerate(colour):
            average[index] += component/number
    return(average)

def collectAndAverageSamples(original, x, y, widthRatio, heightRatio):
    return(tripletAverage([original[widthRatio*x+i][heightRatio*y+j] \
        for i in range(heightRatio) for j in range(widthRatio)]))

def downScaleImage(original, newWidth, newHeight):
    """Scales an image from a 3D array.

    """
    oldWidth = len(original)
    oldHeight = len(original[0])

    assert oldWidth >= newWidth
    assert oldHeight >= newHeight

    #First version doing integer conversion only
    assert oldWidth % newWidth == 0
    assert oldHeight % newHeight == 0

    widthRatio = oldWidth//newWidth
    heightRatio = oldHeight//newHeight

    # collect all the rbg values
    newImg = [ [ collectAndAverageSamples(original,x,y,widthRatio,heightRatio) \
            for y in range(newHeight)] for x in range(newWidth)]
    return(newImg)
