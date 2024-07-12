# GenPhylo: Generating Data on Phylogenetic trees

### Authors: Marta Casanellas, Martí Cortada, Adrià Dieguez

---

The user has two options depending on which arguments are chosen. But both possibilities need to take as input a tree in the Newick format (with nodes of any degree) with annotated branch lengths.

▶️ **Option 1: Generate $N$ FASTA files with alignments of length $L$ given a tree in a Newick format, providing an experiment name**

For example, for $N = 5$ and $L = 1000$, provided also a Newick tree in a ```.txt``` file and an experiment's name to save the results; just type

```diff
python3 main.py <tree.txt> 5 1000 <name_experiment>
```

▶️ **Option 2: Generate FASTA files with alignments of given lengths $L_1,...,L_d$ given a tree in a Newick format, providing also an experiment name**

For example, for $L_1 = 500$, $L_2 = 1000$ and $L_3 = 10000$, provided also a Newick tree in a ```.txt``` file and an experiment's name to save the results; just type

```diff
python3 main.py <tree.txt> L500 L1000 L10000 <name_experiment>
```

⚠️ Note that in this case, sequence lengths are preceeded by an $L$.




