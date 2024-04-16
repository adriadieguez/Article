from config.inputs import reading 
from utils.matrix_generation import matrix_generation

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