import pandas as pd

FILENAME = "output_default_setting.csv"

# Step 1: Read the file into a pandas DataFrame
df = pd.read_csv(FILENAME, header=None, names=['Link'])

# Step 2: Remove duplicate lines
df_unique = df.drop_duplicates()

# Step 3: Sort the lines if order is important (optional)
df_unique = df_unique.sort_values(by='Link')

# If you want to overwrite the original text file
df_unique.to_csv(FILENAME, index=False, header=False)
