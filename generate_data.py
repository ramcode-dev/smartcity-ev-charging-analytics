import csv
import random
from datetime import datetime, timedelta

# Create synthetic EV charging station log dataset
random.seed(202)

zones = ["North Zone - Tech Park", "South Zone - Residential", "East Zone - Commercial Hub", "West Zone - Highway Corridor", "Central Zone - Metro Station"]
payment_methods = ["UPI / QR", "Credit Card", "RFID Card", "Mobile Wallet", ""]
statuses = ["SUCCESS", "SUCCESS", "SUCCESS", "SUCCESS", "FAILED_PAYMENT", "CHARGER_FAULT"]

header = ["Transaction_ID", "Station_ID", "Zone", "Charging_Duration_Mins", "Energy_Consumed_kWh", "Total_Amount_INR", "Payment_Method", "Transaction_Status", "Timestamp"]

rows = []
for i in range(1, 121):
    tx_id = f"EV_TXN_{8000 + i}"
    station_id = f"STN_{random.randint(101, 115)}"
    zone = random.choice(zones)
    duration = random.randint(15, 180)
    
    # Energy consumed roughly 0.2 to 0.4 kWh per minute
    energy = round(duration * random.uniform(0.2, 0.4), 2)
    # Rate: 15 INR per kWh
    amount = round(energy * 15.0, 2)
    
    pay_method = random.choice(payment_methods)
    status = random.choice(statuses)
    
    # Corrupt some transaction amounts for cleaning demo
    if i % 10 == 0:
        amount = ""
        
    days_ago = random.randint(1, 20)
    hour = random.choice([7, 8, 9, 10, 12, 14, 17, 18, 19, 20, 21, 22])
    minute = random.randint(0, 59)
    timestamp = (datetime.now() - timedelta(days=days_ago, hours=hour, minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")
    
    rows.append([tx_id, station_id, zone, duration, energy, amount, pay_method, status, timestamp])

import os
os.makedirs("dataset", exist_ok=True)
os.makedirs("charts", exist_ok=True)

file_path = "dataset/ev_charging_transactions.csv"
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print(f"EV Charging dataset generated successfully at {file_path} with {len(rows)} records!")
