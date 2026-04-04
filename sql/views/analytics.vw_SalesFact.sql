CREATE VIEW analytics.vw_SalesFact AS
SELECT
    soh.SalesOrderID,
    soh.OrderDate,
    soh.CustomerID,
    soh.TerritoryID,
    st.Name                          AS Territory,
    st.CountryRegionCode             AS Country,
    sod.ProductID,
    p.Name                           AS ProductName,
    pc.Name                          AS Category,
    ps.Name                          AS Subcategory,
    sod.OrderQty,
    sod.UnitPrice,
    sod.UnitPriceDiscount,
    sod.LineTotal,
    soh.TotalDue
FROM Sales.SalesOrderHeader soh
JOIN Sales.SalesOrderDetail sod       ON soh.SalesOrderID = sod.SalesOrderID
JOIN Production.Product p             ON sod.ProductID = p.ProductID
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
JOIN Production.ProductCategory pc    ON ps.ProductCategoryID = pc.ProductCategoryID
JOIN Sales.SalesTerritory st          ON soh.TerritoryID = st.TerritoryID;
