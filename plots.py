import pandas as pd
import matplotlib.pyplot as plt

# Intervals de confiança o boxplots?

# Updated data
branch_lengths = [0.1, 0.1, 0.5, 0.5]
alignment_lengths = [1000, 10000, 1000, 10000]
external_abs_error = [0.009, 0.003, 0.088, 0.05]
external_rel_error = [8.865, 3.47, 17.551, 10.082]
internal_abs_error = [0.01, 0.004, 0.107, 0.071]
internal_rel_error = [9.833, 3.848, 21.494, 14.153]

# Create a DataFrame
data = {
    'Branch Length': branch_lengths,
    'Alignment Length': alignment_lengths,
    'External Absolute Error': external_abs_error,
    'External Relative Error': external_rel_error,
    'Internal Absolute Error': internal_abs_error,
    'Internal Relative Error': internal_rel_error
}

df = pd.DataFrame(data)
print(df)

# Plotting
plt.figure(figsize=(12, 8))

# Plotting each metric
for i, (metric, ylabel) in enumerate([('External Absolute Error', 'Absolute Error'),
                                      ('External Relative Error', 'Relative Error (%)'),
                                      ('Internal Absolute Error', 'Absolute Error'),
                                      ('Internal Relative Error', 'Relative Error (%)')]):
    plt.subplot(2, 2, i+1)
    for branch_length, group in df.groupby('Branch Length'):
        plt.plot(group['Alignment Length'], group[metric], marker='o', label=f'Branch Length: {branch_length}')
    
    plt.title(f'{metric.replace("Error", "")} for Branch Length')
    plt.xlabel('Alignment Length')
    plt.ylabel(ylabel)
    plt.legend()

plt.tight_layout()
plt.show()
