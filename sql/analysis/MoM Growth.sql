USE AdventureWorks2022;
GO

WITH MonthlyRevenue AS (
    SELECT
        DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1) AS MonthStart,
        CAST(ROUND(SUM(LineTotal), 2) AS DECIMAL(18,2)) AS Revenue
    FROM analytics.vw_SalesFact
    GROUP BY DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1)
)
SELECT
    MonthStart,
    CAST(Revenue AS DECIMAL(18,2))                                            AS Revenue,
    CAST(LAG(Revenue) OVER (ORDER BY MonthStart) AS DECIMAL(18,2))            AS PrevMonthRevenue,
    CAST(ROUND(
        100.0 * (Revenue - LAG(Revenue) OVER (ORDER BY MonthStart))
              / NULLIF(LAG(Revenue) OVER (ORDER BY MonthStart), 0), 2
    ) AS DECIMAL(10,2))                                                       AS MoM_GrowthPct,
    CAST(SUM(Revenue) OVER (ORDER BY MonthStart ROWS UNBOUNDED PRECEDING) AS DECIMAL(18,2)) AS RunningTotal
FROM MonthlyRevenue
ORDER BY MonthStart;
 
