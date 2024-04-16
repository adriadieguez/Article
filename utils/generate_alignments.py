from model.mathmodel import *
import numpy as np
import os
import tarfile

def generate_alignments(net, node_distribution, edges, length, t, case, lengths):
    """
    Generates alignments based on the given parameters and saves them in FASTA files.
    """
    file_names = []
    tar = tarfile.open("output_files/alignments.tar.gz", "w:gz")

    if case == 1:
        for align in range(t):
            node_sequence = dict()
            node_sequence["Root"] = generate_alignment(length, node_distribution["Root"])
            i = 0
            for edge in net.edges():
                node_sequence[edge[1].name] = generate_sequences(edges[i].transition_matrix,
                                                                 node_sequence[edge[0].name])
                i += 1
            leaves_seq = {k: v for k, v in node_sequence.items() if k.startswith('L')}
            sequences_in_leaves = list(leaves_seq.values())
            keys_for_sequences = list(leaves_seq.keys())
            iter = 0
            file_name = str(len(sequences_in_leaves)) + "_leaves_" + str(
                len(sequences_in_leaves[0])) + "length_sequences_num" + str(
                align + 1) + ".fasta"
            file_names.append(file_name)
            file = open(file_name, "w")
            for seq in sequences_in_leaves:
                file.write(">Seq" + str(keys_for_sequences[iter]) + "\n" + seq + "\n")
                iter += 1
            file.close()
            tar.add(file_name)
            os.remove(file_name)
    else:
        for l in lengths:
            node_sequence = dict()
            node_sequence["Root"] = generate_alignment(l, node_distribution["Root"])
            i = 0
            for edge in net.edges():
                node_sequence[edge[1].name] = generate_sequences(edges[i].transition_matrix,
                                                                 node_sequence[edge[0].name])
                i += 1
            leaves_seq = {k: v for k, v in node_sequence.items() if k.startswith('L')}
            sequences_in_leaves = list(leaves_seq.values())
            keys_for_sequences = list(leaves_seq.keys())
            iter = 0
            file_name = str(len(sequences_in_leaves)) + "_leaves_" + str(
                len(sequences_in_leaves[0])) + "length_sequences.fasta"
            file_names.append(file_name)
            file = open(file_name, "w")
            for seq in sequences_in_leaves:
                file.write(">Seq" + str(keys_for_sequences[iter]) + "\n" + seq + "\n")
                iter += 1
            file.close()
            tar.add(file_name)
            os.remove(file_name)
    tar.close()
    return file_names