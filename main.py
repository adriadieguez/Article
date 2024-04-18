from config.inputs import reading 
from utils.matrix_generation import matrix_generation

_, case, __, ___, name = reading()

if (case == 1):
    tree = _
    L = __
    t = ___
    matrix_generation(tree, L, t, None, case, name)
else:
    tree = _
    lengths = __
    matrix_generation(tree, None, None, lengths, case, name)