-- Smart City EV Charging Usage Analytics Queries

-- 1. Zone revenue and total energy consumption summary
SELECT 
    Zone,
    COUNT(*) AS Total_Sessions,
    SUM(CASE WHEN Transaction_Status = 'SUCCESS' THEN 1 ELSE 0 END) AS Successful_Sessions,
    ROUND(SUM(Energy_Consumed_kWh), 1) AS Energy_kWh,
    ROUND(SUM(Total_Amount_INR), 2) AS Revenue_INR
FROM ev_transactions
GROUP BY Zone
ORDER BY Revenue_INR DESC;


-- 2. Peak hourly charging sessions and duration analysis
SELECT 
    Hour_Of_Day,
    COUNT(*) AS Sessions_Count,
    ROUND(AVG(Charging_Duration_Mins), 1) AS Avg_Duration_Mins,
    ROUND(SUM(Total_Amount_INR), 2) AS Revenue_INR
FROM ev_transactions
WHERE Transaction_Status = 'SUCCESS'
GROUP BY Hour_Of_Day
ORDER BY Sessions_Count DESC;


-- 3. Hardware fault and payment failure rate per station
SELECT 
    Station_ID,
    Zone,
    COUNT(*) AS Total_Attempts,
    SUM(CASE WHEN Transaction_Status != 'SUCCESS' THEN 1 ELSE 0 END) AS Failed_Attempts,
    ROUND(CAST(SUM(CASE WHEN Transaction_Status != 'SUCCESS' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 1) AS Failure_Rate_Pct
FROM ev_transactions
GROUP BY Station_ID, Zone
HAVING Failed_Attempts > 0
ORDER BY Failure_Rate_Pct DESC;
