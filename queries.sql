-- ====================================================================
-- PROJECT 3: SMART CITY EV CHARGING STATION USAGE ANALYTICS
-- SQL QUERIES FOR REVENUE & UTILIZATION METRICS
-- ====================================================================

-- 1. Zone-wise Revenue & Energy Consumption Breakdown
SELECT 
    Zone,
    COUNT(*) AS Total_Sessions,
    SUM(CASE WHEN Transaction_Status = 'SUCCESS' THEN 1 ELSE 0 END) AS Successful_Sessions,
    ROUND(SUM(Energy_Consumed_kWh), 1) AS Total_Energy_kWh,
    ROUND(SUM(Total_Amount_INR), 2) AS Total_Revenue_INR
FROM ev_transactions
GROUP BY Zone
ORDER BY Total_Revenue_INR DESC;


-- 2. Peak Charging Hours & Hourly Utilization Analysis
SELECT 
    Hour_Of_Day,
    COUNT(*) AS Charging_Sessions,
    ROUND(AVG(Charging_Duration_Mins), 1) AS Avg_Duration_Mins,
    ROUND(SUM(Total_Amount_INR), 2) AS Total_Hourly_Revenue
FROM ev_transactions
WHERE Transaction_Status = 'SUCCESS'
GROUP BY Hour_Of_Day
ORDER BY Charging_Sessions DESC;


-- 3. Station Downtime & Failed Payment Analysis
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
