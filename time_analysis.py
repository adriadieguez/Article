import time
import subprocess

def run_command(command):
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    end_time = time.time()
    return end_time - start_time

def main():
    repetitions = 15
    total_time = 0

    command1 = 'python3 main.py tree_8L.txt 5 1000 random a_b_05_8L_1000'

    for i in range(repetitions):
        print(i)
        total_time += run_command(command1)

    avg_time1 = total_time / repetitions

    print("Average execution time:", avg_time1, "seconds")
  
if __name__ == "__main__":
    main()
