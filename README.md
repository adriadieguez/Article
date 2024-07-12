# GenPhylo: Generating Data on Phylogenetic trees

### Authors: Marta Casanellas, Martí Cortada, Adrià Dieguez

---

Our program takes as input a tree in the Newick format (with nodes of any degree) with annotated branch lengths. Moreover, other arguments must be given: the user has two possible options depending on which arguments are chosen,

**Option 1:** <span style="color:blue"> **Generate $N$ FASTA files with alignments of some <em>blue</em> length $L$ given a tree in a newick format, providing an experiment name** </span>

For example, for $N = 5$ and $L = 1000$;
```python3 main.py tree_4L.txt 5 1000 name_experiment```

**Option 2: Generate FASTA files with alignments of given lengths L1...Ld given a tree in a newick format, giving also an experiment name. Note that in this case, sequence lengths are preceeded by an L**

For example, L1 = 500, L2 = 1000 and L3 = 10000;
```python3 main.py tree_4L.txt L500 L1000 L10000 name_experiment```

⚠️



