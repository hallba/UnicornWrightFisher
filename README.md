# Clone wars simulator!

## Introduction

As tissues age, cells
acquire mutations. These mutations can give the cell a selective advantage, 
allowing it to persist or expand in the tissue. Alternatively they may 
put the cell at a disadvantage, or leave it unchanged. 

*Clones* are cells that derive from a single ancestor. As cells are in constant 
competition and continually accrue mutations, clones may gain a mutation and colonize
the tissue. This may however be shortlived, as new clones arise through mutation 
and drive back the original expanding clone. This process may repeat as the
individual ages. Many cancers start growing in this background.

This is a simulator of mutations and aging in normal tissues that runs on a 
raspberry pi or pico and can be visualised with a unicornhat hd or unicorn pico
pack. It can further be connected to external buttons to introduce mutations "live".
Its based on the research my team has been doing on mutations, aging, and cancer.

## Background research 

https://doi.org/10.1016/j.stem.2018.08.017

https://doi.org/10.1098/rsif.2019.0230

https://doi.org/10.1038/s41588-020-0624-3 

## Code authorship

All code unless explicitly noted is written by Ben Hall, b.hall@ucl.ac.uk. 

splash.py is adapted from an example in the @pimoroni repo https://github.com/pimoroni/unicorn-hat-hd