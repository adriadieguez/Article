from config.inputs import reading 
from utils.matrix_generation import matrix_generation

_, case, __, ___, root_distr, name = reading()

if (case == 1):
    tree = _
    t = __
    L = ___
    matrix_generation(tree, L, t, None, case, root_distr, name)
else:
    tree = _
    lengths = __
    matrix_generation(tree, None, None, lengths, case, root_distr, name)
