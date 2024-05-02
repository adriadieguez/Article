import time
import subprocess

def run_command(command):
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    end_time = time.time()
    return end_time - start_time

def run_experiment(tree_file, alignment_length):
    repetitions = 100
    total_time = 0
    branch_length = float(tree_file.split('_')[2][6:8]) / 10   # Extract branch length from file name
    command = f'python3 main.py {tree_file} 1 {alignment_length} random HP_{tree_file}_{alignment_length}'

    for i in range(repetitions):
        total_time += run_command(command)

    avg_time = total_time / repetitions
    print(f"{tree_file} - Branch length {branch_length} - Alignment length {alignment_length} || Avg Time: {avg_time:.2f} seconds")

def main():
    first_command = f'python3 main.py tree_4L_branch01.txt 1 100 random first_exec'
    run_command(first_command)
    trees = ['tree_4L_branch01.txt', 'tree_4L_branch05.txt', 
             'tree_8L_branch01.txt', 'tree_8L_branch05.txt', 
             'tree_16L_branch01.txt', 'tree_16L_branch05.txt']
    alignment_lengths = [1000, 10000]

    for tree in trees:
        for alignment_length in alignment_lengths:
            run_experiment(tree, alignment_length)
  
if __name__ == "__main__":
    main()


