from model.mathmodel import *
import numpy as np

def save_transition_matrices(edges):
    """
    Saves the transition matrices and prints them.
    """
    real_matrices = []
    for e in edges:
        real_matrices.append(MM(e.edge[0].name, e.edge[1].name, e.transition_matrix))
        print(e.edge[0].name, e.edge[1].name)
        print(e.transition_matrix)
        print("**********************************************************************")
    return real_matrices