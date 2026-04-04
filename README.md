# Sales Analytics - SQL Server + Power BI

## Overview
End-to-end business intelligence project analyzing sales performance, customer segmentation, and product trends for AdventureWorks2022, a fictional bicycle manufacturer dataset provided by Microsoft.

Built to demonstrate proficiency in SQL Server, data modeling, DAX, and Power BI dashboard design.

## Dashboard Preview

### Executive Summary
![Executive Summary](screenshots/Executive_Summary.png)

### Customer Analysis
![Customer Analysis](screenshots/Customer_Analysis.png)

### Product Analysis
![Product Analysis](screenshots/Product_Analysis.png)

## Business Questions Answered
- Which products and territories drive the most revenue?
- How is revenue trending month over month and year over year?
- Which customer segments are most valuable using RFM analysis?
- How is revenue distributed across the customer base?

## Technical Stack
| Tool | Purpose |
|---|---|
| SQL Server Express | Database engine |
| SSMS | Query development |
| Power BI Desktop | Data modeling and dashboard |
| DAX | KPI measures and time intelligence |

## Architecture
Raw AdventureWorks Tables
↓
Analytics Schema (SQL Views)
↓
Star Schema Data Model (Power BI)
↓
DAX Measures
↓
Interactive Dashboard
## SQL Layer
Built an `analytics` schema on top of raw AdventureWorks tables with three views:

**vw_SalesFact** - Flat sales fact table joining orders, products, categories and territories into a single analytical layer

**vw_CustomerSummary** - Customer level aggregates including total orders, total revenue, first/last order dates and days since last order

**vw_RFM_Segments** - RFM (Recency, Frequency, Monetary) customer segmentation using NTILE window functions to score and classify customers into six segments: Champion, Loyal, Potential Loyalist, At Risk, Needs Attention, and Lost

### Key SQL Concepts
- CTEs for multi-step analytical queries
- Window functions - `LAG()`, `NTILE()`, `SUM() OVER()`
- `DATEDIFF` and `DATEFROMPARTS` for date calculations
- Month over month growth with divide-by-zero protection via `NULLIF`
- Running totals with `ROWS UNBOUNDED PRECEDING`

## Data Model
Star schema built in Power BI with:
- `vw_SalesFact` as the central fact table
- `vw_CustomerSummary` and `vw_RFM_Segments` as dimension tables
- `DimDate` - custom date dimension table built in Power Query M for time intelligence

## DAX Measures
| Measure | Purpose |
|---|---|
| Total Revenue | `SUM` of LineTotal |
| Total Orders | `DISTINCTCOUNT` of SalesOrderID |
| Total Customers | `DISTINCTCOUNT` of CustomerID |
| Avg Order Value | `DIVIDE` of Revenue by Orders |
| Revenue YTD | Year to date revenue via `TOTALYTD` |
| Revenue LY | Same period last year via `SAMEPERIODLASTYEAR` |
| YoY Growth % | Year over year growth percentage |
| Avg Revenue per Customer | Revenue divided by customer count |
| % of Total Customers | Dynamic segment share using `ALL()` to remove filter context |

## Dashboard Pages

**Executive Summary** - Top level KPIs, revenue trend over time, revenue by product category and sales territory. Year slicer filters all visuals simultaneously.

**Customer Analysis** - RFM segment breakdown via donut chart, revenue by segment, customer revenue distribution showing spend concentration, and key customer metrics. Segment slicer enables filtering by customer type.

**Product Analysis** - Top 10 products by revenue, subcategory treemap, and revenue by category over time showing year over year category performance.

## How to Use
1. Download `powerbi/sales_analytics.pbix`
2. Open in Power BI Desktop
3. The dataset is imported so all visuals are fully interactive without a SQL Server connection
