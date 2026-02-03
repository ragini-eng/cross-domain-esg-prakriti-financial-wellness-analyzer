import pandas as pd
import os

# --- Step 1: Define correct path to dataset ---
# This ensures the script always finds your file, no matter where it's run from
base_dir = os.path.dirname(os.path.abspath(__file__))  # folder of this script
data_path = os.path.join(base_dir, "../data/processed/analytics_ready.csv")

# --- Step 2: Load cleaned dataset ---
try:
    df = pd.read_csv(data_path)
    print("✅ Cleaned data loaded successfully!")
except FileNotFoundError:
    print(f"❌ File not found at: {data_path}")
    exit()

# --- Step 3: Feature 1: ESG Average ---
if all(col in df.columns for col in ["environment_score", "social_score", "governance_score"]):
    df["ESG_Avg"] = df[["environment_score", "social_score", "governance_score"]].mean(axis=1)
else:
    print("⚠️ Some ESG columns are missing!")

# --- Step 4: Feature 2: Financial Health Score ---
if all(col in df.columns for col in ["income", "savings", "expenses"]):
    df["Finance_Health_Score"] = (df["savings"] / (df["expenses"] + 1)) * 100
else:
    df["Finance_Health_Score"] = 0
    print("⚠️ Financial columns missing, default Finance_Health_Score = 0")

# --- Step 5: Feature 3: Prakriti Encoding ---
prakriti_map = {"Vata": 1, "Pitta": 2, "Kapha": 3}
if "prakriti_type" in df.columns:
    df["Prakriti_Index"] = df["prakriti_type"].map(prakriti_map)
else:
    df["Prakriti_Index"] = 0
    print("⚠️ Prakriti type column missing!")

# --- Step 6: Feature 4: Combined Sustainability Alignment ---
df["Sustainability_Score"] = (
    (df.get("ESG_Avg", 0) * 0.6)
    + (df.get("Finance_Health_Score", 0) * 0.3)
    + (df.get("Prakriti_Index", 0) * 10)
)

# --- Step 7: Save processed data ---
output_path = os.path.join(base_dir, "../data/processed/featured_data.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"🎯 Feature engineered data saved successfully at:\n{output_path}")
