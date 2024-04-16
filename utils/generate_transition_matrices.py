from model.mathmodel import *
import numpy as np

def generate_transition_matrices(tree, node_distribution):
    """
    Generates transition matrices for each edge in the phylogenetic tree.
    """
    edges = []
    for edge in tree.edges():
        l = 4 * edge[1].branch_length  # (Lake'94)
        new_edge = Edge(edge, generate_random_matrix(node_distribution[edge[0].name], l))
        edges.append(new_edge)
        node_distribution[edge[1].name] = np.matmul(node_distribution[edge[0].name], new_edge.transition_matrix)
        for i in range(4):
            assert (np.sum(new_edge.transition_matrix[i, :]) < 1.000000001 and np.sum(
                new_edge.transition_matrix[i, :]) > 0.999999999)
    return edges