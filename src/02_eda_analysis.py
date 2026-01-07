import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the Excel file
file_path = 'results/data/correlation_matrix.xlsx'  
df = pd.read_excel(file_path)

# Computing the correlation matrix
corr = df.corr(numeric_only=True)

# Ploting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()

