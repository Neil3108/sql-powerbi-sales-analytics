CREATE VIEW analytics.vw_CustomerSummary AS
SELECT
    c.CustomerID,
    COUNT(DISTINCT soh.SalesOrderID)            AS TotalOrders,
    SUM(sod.LineTotal)                          AS TotalRevenue,
    MIN(soh.OrderDate)                          AS FirstOrderDate,
    MAX(soh.OrderDate)                          AS LastOrderDate,
    DATEDIFF(DAY, MAX(soh.OrderDate), GETDATE()) AS DaysSinceLastOrder
FROM Sales.Customer c
JOIN Sales.SalesOrderHeader soh ON c.CustomerID = soh.CustomerID
JOIN Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
GROUP BY c.CustomerID;
