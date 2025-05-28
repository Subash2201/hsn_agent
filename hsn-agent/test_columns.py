from utils import load_master_data

# Load and print first few rows
df = load_master_data()
print("Column names:", df.columns.tolist())
print(df.head())
