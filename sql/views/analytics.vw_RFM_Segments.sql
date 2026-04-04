CREATE VIEW analytics.vw_RFM_Segments AS
WITH RFM_Base AS (
    SELECT
        CustomerID,
        DATEDIFF(DAY, MAX(OrderDate), GETDATE())  AS Recency,
        COUNT(DISTINCT SalesOrderID)               AS Frequency,
        SUM(TotalDue)                              AS Monetary
    FROM Sales.SalesOrderHeader
    GROUP BY CustomerID
),
RFM_Scored AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY Recency ASC)    AS R_Score,
        NTILE(5) OVER (ORDER BY Frequency DESC) AS F_Score,
        NTILE(5) OVER (ORDER BY Monetary DESC)  AS M_Score
    FROM RFM_Base
)
SELECT *,
    CONCAT(R_Score, F_Score, M_Score) AS RFM_Cell,
    CASE
        WHEN R_Score >= 4 AND F_Score >= 4 THEN 'Champion'
        WHEN R_Score >= 3 AND F_Score >= 3 THEN 'Loyal'
        WHEN R_Score >= 3 AND F_Score <= 2 THEN 'Potential Loyalist'
        WHEN R_Score <= 2 AND F_Score >= 3 THEN 'At Risk'
        WHEN R_Score = 1 AND F_Score = 1  THEN 'Lost'
        ELSE 'Needs Attention'
    END AS CustomerSegment
FROM RFM_Scored;
