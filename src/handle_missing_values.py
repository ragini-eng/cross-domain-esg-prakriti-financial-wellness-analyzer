import os
import pandas as pd

# --- Step 1: Define folder and filename separately ---
folder = r"C:\Users\Ajay Singh Pawaiya\Desktop\esg_prakriti_analyzer\data\processed"
filename = "analytics_ready_with_missing_columns.csv"  # use the actual filename with (1)
file_path = os.path.join(folder, filename)

# --- Step 2: Check if file exists and load CSV ---
if os.path.isfile(file_path):
    print("File found! Loading CSV...")
    df = pd.read_csv(file_path)
    print("CSV loaded successfully. First 5 rows:")
    print(df.head())
else:
    print("❌ File not found!")
    print("Files in folder:", os.listdir(folder))
    exit()  # stop script if file not found

# --- Step 3: Check for missing values ---
print("\nMissing values per column before cleaning:")
print(df.isnull().sum())

# --- Step 4a: Fill numeric columns with mean ---
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# --- Step 4b: Fill categorical columns with mode ---
categorical_cols = df.select_dtypes(include='object').columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# --- Step 5: Save cleaned CSV ---
cleaned_filename = "analytics_ready_cleaned.csv"
df.to_csv(os.path.join(folder, cleaned_filename), index=False)
print(f"\n✅ CSV cleaned and saved as {cleaned_filename}")

