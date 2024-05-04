from model.mathmodel import *
import numpy as np

def DLC(matrix):
    B = True
    for j in range(matrix.shape[1]):
        max_index = np.argmax(matrix[:, j])
        if max_index != j:
            B = False
    return B

def generate_transition_matrices(tree, node_distribution):
    """
    Generates transition matrices for each edge in the phylogenetic tree.
    """
    edges = []
    for edge in tree.edges():
        l = 4 * edge[1].branch_length  # (Lake'94)
        matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        while not DLC(matrix):
            #print("Checking DLC")
            matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        new_edge = Edge(edge, matrix)
        edges.append(new_edge)
        node_distribution[edge[1].name] = np.matmul(node_distribution[edge[0].name], new_edge.transition_matrix)
        for i in range(4):
            assert (np.sum(new_edge.transition_matrix[i, :]) < 1.000000001 and np.sum(
                new_edge.transition_matrix[i, :]) > 0.999999999)
    return edges