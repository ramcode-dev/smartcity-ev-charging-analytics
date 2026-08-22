# Smart City EV Charging Station Usage & Revenue Analytics

## 📌 Project Overview
An urban mobility analytics project evaluating EV charging station usage, energy consumption patterns, and peak charging hour demand across smart city zones.

Designed for **Smart City & Green Mobility Analytics** (aligned with MeitY Smart City Initiatives).

---

## 🛠️ Tech Stack & Skills
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy, Datetime
* **Query Engine:** SQL (SQLite / SQLite3)
* **Visualization:** Matplotlib
* **Format:** CSV

---

## 📊 Key Insights & Analytical Results
1. **Data Imputation & Feature Engineering:** Calculated missing transaction amounts based on kWh rates, extracted `Hour_Of_Day` timestamp features.
2. **Revenue Analytics:** Identified highest revenue zones (*Tech Park* and *Highway Corridor*).
3. **Operational Reliability:** Flagged chargers experiencing recurring payment errors and hardware faults.

---

## 🚀 How to Run

1. Clone repository:
```bash
git clone <your-repo-link>
cd project3_smartcity_ev_charging_analytics
```

2. Run automated pipeline:
```bash
python generate_data.py
python analysis.py
```

3. View generated outputs:
* CSV Dataset: `dataset/ev_charging_transactions.csv`
* Chart Output: `charts/zone_revenue_breakdown.png`
* SQL Scripts: `queries.sql`
