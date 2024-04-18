from model.mathmodel import *
import numpy as np

def save_transition_matrices(edges, name):
    """
    Saves the transition matrices and prints them.
    """
    real_matrices = []
    output_file = "output_files/" + name + "_transition_matrices.txt"
    with open(output_file, "w") as f:
        for e in edges:
            f.write(e.edge[0].name + " " + e.edge[1].name + "\n")
            f.write(str(e.transition_matrix) + "\n")
            f.write("**********************************************************************\n")
    return real_matrices