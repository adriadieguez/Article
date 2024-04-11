import os
import tarfile
from model.mathmodel import *

def matrix_generation(tree, length, t, lengths, case):
    """
    We propagate the matrices generation along the tree
    by calling the prior methods for every tree edge.
    """
    node_distribution = dict()
    B = False

    # Root distribution generation
    while not B:
        R = np.random.dirichlet([1, 1, 1, 1])
        Res = all(ele > 0.2 and ele < 0.3 for ele in R)
        if Res == True:
            B = True
    node_distribution["Root"] = R

    # Reading the phylogenetic tree (input: Newick format)
    path_t = tree
    tree_file = open(path_t, "r")
    tree = tree_file.read()
    tree = Phylo.read(StringIO(tree), "newick")
    # Adapt node names
    for idx, clade in enumerate(tree.get_nonterminals()):
        clade.name = "Node_" + str(idx) if idx > 0 else "Root"
    # Adapt leaf names
    for idx, clade in enumerate(tree.get_terminals()):
        clade.name = "Leaf_" + clade.name
    # Phylogenetic tree to graph
    net = Phylo.to_networkx(tree)

    iter = 0
    edges = []
    # Propagation
    for edge in net.edges():
        l = 4*edge[1].branch_length # (Lake'94)
        # Generate transition matrix
        new_edge = Edge(edge, generate_random_matrix(
                        node_distribution[edge[0].name], l))
        edges.append(new_edge)
        # Descendant distribution
        node_distribution[edge[1].name] = np.matmul(
                    node_distribution[edge[0].name],new_edge.transition_matrix)
        for i in range(4):
            assert(np.sum(new_edge.transition_matrix[i,:])<1.000000001 and np.sum(
                   new_edge.transition_matrix[i,:])>0.999999999)
        iter += 1

    assert(iter == len(net.edges()))

    # Save all the transition matrices
    real_matrices = []
    for e in edges:
        real_matrices.append(MM(e.edge[0].name, e.edge[1].name, e.transition_matrix))
        print(e.edge[0].name, e.edge[1].name)
        print(e.transition_matrix)
        print("**********************************************************************")


    # Generating the alignments and saving them in FASTA files in a TAR.
    file_names = []
    tar = tarfile.open("alignments.tar.gz", "w:gz")

    # Case 1: Once the transition matrices are computed,
    # we generate t alignments of length L using the same matrices.
    if case == 1:

        for align in range(t):

            node_sequence = dict()
            node_sequence["Root"] = generate_alignment(length, node_distribution["Root"])
            i = 0
            for edge in net.edges():
                # Generating each sequence
                node_sequence[edge[1].name] = generate_sequences(
                             edges[i].transition_matrix, node_sequence[edge[0].name])
                i += 1

            leaves_seq = {k: v for k, v in node_sequence.items() if k.startswith('L')}
            sequences_in_leaves = list(leaves_seq.values())
            keys_for_sequences = list(leaves_seq.keys())
            iter = 0
            file_name = str(len(sequences_in_leaves))+ "_leaves_" + str(
                        len(sequences_in_leaves[0])) + "length_sequences_num" + str(
                        align+1) +".fasta"
            file_names.append(file_name)
            file = open(file_name, "w")
            # Write in the FASTA file
            for seq in sequences_in_leaves:
                file.write(">Seq" + str(keys_for_sequences[iter]) + "\n" + seq + "\n")
                iter += 1
            file.close()
            tar.add(file_name)
            os.remove(file_name)

    # Case 2: Once the transition matrices are computed,
    # we generate alignments with lengths L1...Ld
    else:
        for l in lengths:
            node_sequence = dict()
            node_sequence["Root"] = generate_alignment(l, node_distribution["Root"])
            i = 0
            for edge in net.edges():
                # Generating each sequence
                node_sequence[edge[1].name] = generate_sequences(
                              edges[i].transition_matrix, node_sequence[edge[0].name])
                i += 1

            leaves_seq = {k: v for k, v in node_sequence.items() if k.startswith('L')}
            sequences_in_leaves = list(leaves_seq.values())
            keys_for_sequences = list(leaves_seq.keys())
            iter = 0
            file_name = str(len(sequences_in_leaves))+ "_leaves_" + str(
                            len(sequences_in_leaves[0])) + "length_sequences.fasta"
            file_names.append(file_name)
            file = open(file_name, "w")
            # Write in the FASTA file
            for seq in sequences_in_leaves:
                file.write(">Seq" + str(keys_for_sequences[iter]) + "\n" + seq + "\n")
                iter += 1
            file.close()
            tar.add(file_name)
            os.remove(file_name)

    tar.close()
    return real_matrices, file_names

