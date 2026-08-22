# Smart City EV Charging Usage Analytics

An urban mobility data analytics project evaluating charging station usage logs, peak charging hours, and revenue distribution across city zones.

## Overview
As electric vehicle adoption grows, municipal infrastructure requires data-driven insights to manage station load and plan grid distribution. This repository processes EV charging transaction logs to track energy consumption (kWh) and station availability.

## Technical Workflow
1. **Data Cleaning & Imputation:** Imputed missing billing amounts using base kWh rates (₹15/kWh); extracted hourly timestamp metrics.
2. **Zone Aggregations:** Grouped charging sessions by municipal zone to measure overall revenue and session success rates.
3. **Peak Hour Analysis:** Used SQL queries to identify high-volume charging hours across city hubs.
4. **Visualization:** Plotting horizontal bar charts of revenue generated per zone using Matplotlib.

## Repository Contents
* `dataset/ev_charging_transactions.csv`: Raw transaction dataset.
* `analysis.py`: Main python processing script.
* `queries.sql`: Standalone SQL query scripts.
* `charts/zone_revenue_breakdown.png`: Revenue distribution visual chart.

## How to Run
```bash
python analysis.py
```
