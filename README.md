# Sales Analytics - SQL Server + Power BI + Streamlit

## Overview
End-to-end business intelligence project analyzing sales performance, customer segmentation, and product trends for AdventureWorks2022, a fictional bicycle manufacturer dataset provided by Microsoft.

Built to demonstrate proficiency in SQL Server, data modeling, DAX, and Power BI dashboard design.

## Interactive App
Explore the fully interactive version of this dashboard:

[View Live Dashboard](https://sql-powerbi-sales-analytics-rrs2rxsbejear2mxdznyua.streamlit.app/)

Built with Streamlit and Plotly - no setup required, runs in your browser.

## Dashboard Preview

### Executive Summary
![Executive Summary](https://github.com/Neil3108/sql-powerbi-sales-analytics/blob/main/screenshots/Executive%20Summary.png)

### Customer Analysis
![Customer Analysis](https://github.com/Neil3108/sql-powerbi-sales-analytics/blob/main/screenshots/Customer%20Analysis.png)

### Product Analysis
![Product Analysis](https://github.com/Neil3108/sql-powerbi-sales-analytics/blob/main/screenshots/Product%20Analysis.png)

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
| Python + Streamlit | Interactive web dashboard |
| Plotly | Interactive chart library |
| Pandas | Data manipulation |

## Architecture
Raw AdventureWorks Tables

↓

Analytics Schema (SQL Views)

↓

Star Schema Data Model (Power BI)

↓

DAX Measures → Power BI Dashboard (.pbix)

↓

CSV Export → Streamlit App (Live URL)

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
### Option 1 — Live Streamlit App (Recommended)
[View Live Dashboard](https://sql-powerbi-sales-analytics-rrs2rxsbejear2mxdznyua.streamlit.app/) — no setup required

### Option 2 — Power BI Desktop
1. Download `powerbi/sales_analytics.pbix`
2. Open in Power BI Desktop (free at powerbi.microsoft.com)
3. All data is imported — fully interactive without any additional setup