import pandas as pd
import numpy as np

# 1️⃣ Load the raw datasets
import os
file_path = os.path.join(os.getcwd(), "data", "raw", "prakriti_profiles_100.csv")
prakriti_df = pd.read_csv(file_path)
file_path = os.path.join(os.getcwd(), "data", "raw", "Personal_Finance_Dataset.csv")
finance_df = pd.read_csv(file_path)
file_path = os.path.join(os.getcwd(), "data", "raw", "company_esg_financial_dataset.csv")
esg_df = pd.read_csv(file_path)

print("✅ Data Loaded Successfully!")

# 2️⃣ Remove Duplicates
prakriti_df.drop_duplicates(inplace=True)
finance_df.drop_duplicates(inplace=True)
esg_df.drop_duplicates(inplace=True)

print("✅ Duplicates Removed!")

# 3️⃣ Handle Missing Values
prakriti_df.fillna("Unknown", inplace=True)
finance_df.fillna(finance_df.mean(numeric_only=True), inplace=True)
esg_df.fillna(esg_df.mean(numeric_only=True), inplace=True)

print("✅ Missing values handled!")

# 4️⃣ Standardize Column Names
def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("[^a-zA-Z0-9_]", "", regex=True)
    )
    return df

prakriti_df = clean_columns(prakriti_df)
finance_df = clean_columns(finance_df)
esg_df = clean_columns(esg_df)

print("✅ Column names standardized!")

# 5️⃣ Fix Data Types (convert numbers stored as text)
for df in [finance_df, esg_df]:
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")

print("✅ Data types fixed!")

# 6️⃣ Remove Outliers (example for income)
if "income" in finance_df.columns:
    upper_limit = finance_df["income"].quantile(0.99)
    finance_df = finance_df[finance_df["income"] <= upper_limit]

print("✅ Outliers handled!")

# 7️⃣ Merge all datasets (if a common ID exists)
if "user_id" in finance_df.columns and "user_id" in prakriti_df.columns:
    merged_df = pd.merge(prakriti_df, finance_df, on="user_id", how="inner")
else:
    merged_df = prakriti_df.join(finance_df, how="outer")

# Just add ESG data if key exists
if "company_id" in esg_df.columns and "company_id" in merged_df.columns:
    merged_df = pd.merge(merged_df, esg_df, on="company_id", how="left")

print("✅ Datasets merged successfully!")

# 8️⃣ Save Clean Data



# Dynamically find project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
processed_dir = os.path.join(project_root, "data", "processed")

# Create folder if not exists
os.makedirs(processed_dir, exist_ok=True)

# Save cleaned file
output_path = os.path.join(processed_dir, "analytics_ready.csv")
merged_df.to_csv(output_path, index=False)
print(f"✅ Cleaned data saved successfully at: {output_path}")

print("🎯 Cleaned and merged data saved to data/processed/analytics_ready.csv")
