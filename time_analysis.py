import time
import subprocess

def run_command(command):
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    end_time = time.time()
    return end_time - start_time

def main():
    repetitions = 50
    total_time = 0

    command1 = "python3 GenGM_orig.py tree_4L.txt 10 1000"

    for _ in range(repetitions):
        total_time1 += run_command(command1)

    avg_time1 = total_time1 / repetitions
    avg_time2 = total_time2 / repetitions

    print("Average execution time:", avg_time1, "seconds")
  
if __name__ == "__main__":
    main()
