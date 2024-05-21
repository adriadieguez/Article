import os
import subprocess
import tarfile
import shutil
import re
import statistics

def run_command(command, suppress_output=False):
    try:
        if suppress_output:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        raise

def expand_user_path(path):
    return os.path.expanduser(path)

def extract_tarfile(tar_path, extract_dir):
    try:
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=extract_dir)
    except (tarfile.TarError, FileNotFoundError) as e:
        print(f"Extraction failed with error: {e}")
        raise

def parse_tree(tree_content):
    """Parses the tree content to extract branch lengths."""
    tree_content = tree_content.replace('\n', '').replace(' ', '')

    branch_lengths = re.findall(r':([0-9.]+)', tree_content)

    external_branch_length = branch_lengths[0]
    internal_branch_length = branch_lengths[-1]

    last_internal_match = re.search(r'\)(:[0-9.]+)', tree_content)
    if last_internal_match:
        internal_branch_length = last_internal_match.group(1)[1:]

    return float(external_branch_length), float(internal_branch_length)

def extract_treefile(output_dir, alignment_file, true_branch_length):
    treefile = os.path.join(output_dir, f'{alignment_file}.treefile')
    if os.path.exists(treefile):
        destination = os.path.join(output_dir, 'estimated_tree.treefile')
        shutil.copyfile(treefile, destination)
        
        with open(destination, 'r') as file:
            tree_content = file.read()
            
            external_branch_length, internal_branch_length = parse_tree(tree_content)
            
            abs_error_external = abs(external_branch_length - true_branch_length)
            rel_error_external = (abs_error_external / true_branch_length) * 100

            abs_error_internal = abs(internal_branch_length - true_branch_length)
            rel_error_internal = (abs_error_internal / true_branch_length) * 100

            return (external_branch_length, internal_branch_length, abs_error_external, rel_error_external, abs_error_internal, rel_error_internal)
    else:
        print(f"Tree file not found: {treefile}")
        raise FileNotFoundError(f"{treefile} does not exist")

def main():
    iqtree_path = expand_user_path('C:\\Users\\diegu\\Desktop\\Programes\\IQTREE\\iqtree-2.3.2-Windows\\bin\\iqtree2.exe')
    fasta_filename_template = '4_leaves_{alignment_length}length_sequences_num1.fasta'
    
    branch_lengths = [0.1, 0.5]
    alignment_lengths = [1000, 10000]

    num_experiments = 100

    for branch_length in branch_lengths:
        tree_file = 'tree_4L_branch01.txt' if branch_length == 0.1 else 'tree_4L_branch05.txt'
        
        for alignment_length in alignment_lengths:
            external_branch_lengths = []
            internal_branch_lengths = []
            abs_errors_external = []
            rel_errors_external = []
            abs_errors_internal = []
            rel_errors_internal = []
            
            for _ in range(num_experiments):
                fasta_filename = fasta_filename_template.format(alignment_length=alignment_length)
                tar_path = os.path.join('output_files', f'HP_{tree_file}_{alignment_length}_alignments.tar.gz')
                extracted_path = os.path.join('output_files', 'IQTTREE_Analysis', f'{branch_length} Length{alignment_length}', fasta_filename)
                
                sim_command = f'python3 main.py {tree_file} 1 {alignment_length} random HP_{tree_file}_{alignment_length}'
                run_command(sim_command)
                
                extract_tarfile(tar_path, os.path.dirname(extracted_path))
                
                iqtree_command = f'"{iqtree_path}" -s "{extracted_path}" -m 012345 -z tree_4L_nolengths.txt --redo'
                run_command(iqtree_command, suppress_output=True)
                
                output_dir = os.path.dirname(extracted_path)
                results = extract_treefile(output_dir, fasta_filename, branch_length)
                
                external_branch_lengths.append(results[0])
                internal_branch_lengths.append(results[1])
                abs_errors_external.append(results[2])
                rel_errors_external.append(results[3])
                abs_errors_internal.append(results[4])
                rel_errors_internal.append(results[5])
            
            avg_external_branch_length = round(statistics.mean(external_branch_lengths), 3)
            avg_internal_branch_length = round(statistics.mean(internal_branch_lengths), 3)
            avg_abs_error_external = round(statistics.mean(abs_errors_external), 3)
            avg_rel_error_external = round(statistics.mean(rel_errors_external), 3)
            avg_abs_error_internal = round(statistics.mean(abs_errors_internal), 3)
            avg_rel_error_internal = round(statistics.mean(rel_errors_internal), 3)

            print(f"Branch length: {branch_length}, Alignment length: {alignment_length}")
            print(f"Average estimated external branch length: {avg_external_branch_length}")
            print(f"Average estimated internal branch length: {avg_internal_branch_length}")
            print(f"Average absolute error for external branch length: {avg_abs_error_external}")
            print(f"Average relative error for external branch length: {avg_rel_error_external}%")
            print(f"Average absolute error for internal branch length: {avg_abs_error_internal}")
            print(f"Average relative error for internal branch length: {avg_rel_error_internal}%")
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
