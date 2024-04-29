import os
import tarfile
import json
from io import StringIO
import networkx as nx
from Bio import Phylo

tree_file = open("./tree_4L.txt", "r")
tree = tree_file.read()
tree = Phylo.read(StringIO(tree), "newick")

# Define a function to label internal nodes with their index
def label_internal_nodes(tree):
    idx = 0
    for clade in tree.find_clades(order='postorder'):
        if not clade.is_terminal():
            clade.name = f"internal_{idx}"
            idx += 1

# Label internal nodes
label_internal_nodes(tree)

# Convert the tree to Newick format with internal node labels
newick_with_labels = StringIO()
Phylo.write(tree, newick_with_labels, "newick")

# Get the Newick string with internal node labels
newick_with_labels_str = newick_with_labels.getvalue()

# Print the Newick string with internal node labels
print(newick_with_labels_str)