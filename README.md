# MA-Phylo by Martí Cortada and Adrià Diéguez

## GenGM.py

**Option 1: Generate t FASTA files with alignments of length L given a tree in a newick format, giving also an experiment name**

For example, t = 5 and L = 1000;
```python3 main.py tree_4L.txt 5 1000 name_experiment```

**Option 2: Generate FASTA files with alignments of given lengths L1...Ld given a tree in a newick format, giving also an experiment name. Note that in this case, sequence lengths are preceeded by an L**

For example, L1 = 500, L2 = 1000 and L3 = 10000;
```python3 main.py tree_4L.txt L500 L1000 L10000 name_experiment```


## Experiments: Martí 
4 branches: generating 5 fasta files for the following scenarios:

* length 1000: 

$a=b=0.1$ Average execution time: 1.4265469598770142 seconds,

$a=b=0.5$ Average execution time: 3.0718810176849365 seconds

---

* length 10000: 

$a=b=0.1$ Average execution time: 2.9485430765151976 seconds, 

$a=b=0.5$ Average execution time: 2.9974852848052977 seconds


