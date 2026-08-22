"""
Smart City EV Charging Station Usage Analytics

Author: Ram
Description: Analysis of EV charging station transactions, peak usage hours, and revenue
            distribution across smart city zones.
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "ev_charging_transactions.csv")
CHART_PATH = os.path.join(BASE_DIR, "charts", "zone_revenue_breakdown.png")


def process_ev_data(filepath):
    df = pd.read_csv(filepath)

    # Recalculate missing transaction amounts from kWh consumed (rate: 15 INR / kWh)
    df["Total_Amount_INR"] = pd.to_numeric(df["Total_Amount_INR"], errors="coerce")
    df["Total_Amount_INR"] = df["Total_Amount_INR"].fillna(df["Energy_Consumed_kWh"] * 15.0).round(2)

    # Fill missing payment methods
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown").replace({"": "Unknown"})

    # Parse timestamps and extract hour of day
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Hour_Of_Day"] = df["Timestamp"].dt.hour

    return df


def execute_sql_insights(df):
    conn = sqlite3.connect(":memory:")
    df.to_sql("ev_transactions", conn, index=False, if_exists="replace")

    query_zone = """
    SELECT 
        Zone,
        COUNT(*) AS Total_Sessions,
        SUM(CASE WHEN Transaction_Status = 'SUCCESS' THEN 1 ELSE 0 END) AS Successful_Sessions,
        ROUND(SUM(Energy_Consumed_kWh), 1) AS Energy_kWh,
        ROUND(SUM(Total_Amount_INR), 2) AS Revenue_INR
    FROM ev_transactions
    GROUP BY Zone
    ORDER BY Revenue_INR DESC;
    """

    query_peak = """
    SELECT 
        Hour_Of_Day,
        COUNT(*) AS Sessions_Count,
        ROUND(AVG(Charging_Duration_Mins), 1) AS Avg_Duration_Mins,
        ROUND(SUM(Total_Amount_INR), 2) AS Revenue_INR
    FROM ev_transactions
    WHERE Transaction_Status = 'SUCCESS'
    GROUP BY Hour_Of_Day
    ORDER BY Sessions_Count DESC;
    """

    zone_summary = pd.read_sql_query(query_zone, conn)
    peak_hours = pd.read_sql_query(query_peak, conn)
    conn.close()

    return zone_summary, peak_hours


def plot_revenue_by_zone(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    zone_rev = df.groupby("Zone")["Total_Amount_INR"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    zone_rev.plot(kind="barh", color="#337ab7", ax=ax, edgecolor="#2e6da4", alpha=0.85)

    ax.set_title("Total Revenue (INR) Generated per Smart City Zone", fontsize=11, fontweight="bold")
    ax.set_xlabel("Revenue (INR)", fontsize=9)
    ax.set_ylabel("Zone", fontsize=9)
    plt.grid(axis="x", linestyle=":", alpha=0.6)

    for i, val in enumerate(zone_rev):
        ax.text(val + 150, i, f"₹{val:,.0f}", va="center", fontsize=8.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing dataset at {DATA_PATH}")

    df = process_ev_data(DATA_PATH)
    zone_df, peak_df = execute_sql_insights(df)

    print("--- Zone Revenue & Session Summary ---")
    print(zone_df.to_string(index=False))

    print("\n--- Peak Hourly Utilization ---")
    print(peak_df.to_string(index=False))

    plot_revenue_by_zone(df, CHART_PATH)
    print(f"\nSaved revenue chart to {CHART_PATH}")


if __name__ == "__main__":
    main()
