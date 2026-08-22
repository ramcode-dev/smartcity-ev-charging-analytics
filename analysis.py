import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)
os.makedirs("dataset", exist_ok=True)

if not os.path.exists("dataset/ev_charging_transactions.csv"):
    import generate_data

print("==================================================================")
print("  PROJECT 3: SMART CITY EV CHARGING STATION USAGE ANALYTICS")
print("==================================================================")

# 1. Load Raw Dataset
df = pd.read_csv("dataset/ev_charging_transactions.csv")
print(f"\n[STEP 1] Loaded raw EV charging dataset: {len(df)} records found.")

# 2. Data Cleaning
print("\n[STEP 2] Performing Data Cleaning & Imputation...")
df['Total_Amount_INR'] = pd.to_numeric(df['Total_Amount_INR'], errors='coerce')
# Impute missing amounts using Energy_Consumed_kWh * 15.0 INR
df['Total_Amount_INR'] = df['Total_Amount_INR'].fillna(df['Energy_Consumed_kWh'] * 15.0).round(2)

df['Payment_Method'] = df['Payment_Method'].fillna('UNKNOWN')
df['Payment_Method'] = df['Payment_Method'].replace({'': 'UNKNOWN'})

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour_Of_Day'] = df['Timestamp'].dt.hour
print("Data Cleaning Complete. Missing billing amounts recalculated & Hour of Day extracted.")

# 3. SQL Analytics
print("\n[STEP 3] Running SQL Analytics using SQLite Database...")
conn = sqlite3.connect(":memory:")
df.to_sql("ev_transactions", conn, index=False, if_exists="replace")

# SQL Query 1: Zone-wise Revenue & Energy Consumption
query_zone = """
SELECT 
    Zone,
    COUNT(*) AS Total_Sessions,
    SUM(CASE WHEN Transaction_Status = 'SUCCESS' THEN 1 ELSE 0 END) AS Successful_Sessions,
    ROUND(SUM(Energy_Consumed_kWh), 1) AS Total_Energy_kWh,
    ROUND(SUM(Total_Amount_INR), 2) AS Total_Revenue_INR
FROM ev_transactions
GROUP BY Zone
ORDER BY Total_Revenue_INR DESC;
"""
df_zone_result = pd.read_sql_query(query_zone, conn)
print("\n--- SQL Query Result: Zone-wise Revenue & Energy Summary ---")
print(df_zone_result.to_string(index=False))

# SQL Query 2: Peak Charging Hours
query_peak = """
SELECT 
    Hour_Of_Day,
    COUNT(*) AS Charging_Sessions,
    ROUND(AVG(Charging_Duration_Mins), 1) AS Avg_Duration_Mins,
    ROUND(SUM(Total_Amount_INR), 2) AS Total_Hourly_Revenue
FROM ev_transactions
WHERE Transaction_Status = 'SUCCESS'
GROUP BY Hour_Of_Day
ORDER BY Charging_Sessions DESC;
"""
df_peak_result = pd.read_sql_query(query_peak, conn)
print("\n--- SQL Query Result: Peak Charging Hours Breakdown ---")
print(df_peak_result.to_string(index=False))

# 4. Data Visualization
print("\n[STEP 4] Generating Data Visualization Chart...")
plt.figure(figsize=(9, 5))
zone_rev = df.groupby('Zone')['Total_Amount_INR'].sum().sort_values(ascending=True)

zone_rev.plot(kind='barh', color='#3498db', edgecolor='black', alpha=0.85, figsize=(9, 5))
plt.title("Total Revenue (INR) Generated Across Smart City Zones", fontsize=12, fontweight='bold')
plt.xlabel("Total Revenue (INR)", fontsize=10)
plt.ylabel("Smart City Zone", fontsize=10)
plt.grid(axis='x', linestyle='--', alpha=0.7)

for idx, val in enumerate(zone_rev):
    plt.text(val + 100, idx, f"₹{val:,.0f}", va='center', fontweight='bold')

plt.tight_layout()
chart_path = "charts/zone_revenue_breakdown.png"
plt.savefig(chart_path, dpi=300)
plt.close()
print(f"Chart saved successfully at: {chart_path}")

print("\n==================================================================")
print("  PROJECT 3 ANALYSIS COMPLETE! Output generated successfully.")
print("==================================================================")
