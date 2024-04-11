from config.reading_konsole import reading 
from utils.utils import matrix_generation

_, __, ___, ____ = reading()
case = __ 

if (case == 1):
    tree = _
    L = ___
    t = ____
    matrix_generation(tree, L, t, None, case)
else:
    tree = _
    lengths = ___
    matrix_generation(tree, None, None, lengths, case)