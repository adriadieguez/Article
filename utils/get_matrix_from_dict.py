import numpy as np

def get_matrix_from_dict(d):
    """
    Returns a 4x4 matrix given a dictionary with 16 values
    """
    Q2 = np.zeros((4,4))
    coefficients = list(d.values())
    for i in range(4):
        for j in range(4):
            Q2[i,j] = coefficients[i*4+j]
    return Q2