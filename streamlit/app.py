import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    sales = pd.read_csv("streamlit/data/sales_fact.csv")
    customers = pd.read_csv("streamlit/data/customer_summary.csv")
    rfm = pd.read_csv("streamlit/data/rfm_segments.csv")
    mom = pd.read_csv("streamlit/data/mom_growth.csv")
    
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    mom["MonthStart"] = pd.to_datetime(mom["MonthStart"])
    
    return sales, customers, rfm, mom

sales, customers, rfm, mom = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Executive Summary", "Customer Analysis", "Product Analysis"]
)

# --- Pages ---
if page == "Executive Summary":
    st.title("📊 Executive Summary")

    # --- Year Filter ---
    years = sorted(sales["OrderDate"].dt.year.unique())
    selected_years = st.multiselect(
        "Filter by Year", years, default=years
    )
    filtered_sales = sales[sales["OrderDate"].dt.year.isin(selected_years)]
    filtered_mom = mom[mom["MonthStart"].dt.year.isin(selected_years)]

    # --- KPI Cards ---
    total_revenue = filtered_sales["LineTotal"].sum()
    total_orders = filtered_sales["SalesOrderID"].nunique()
    total_customers = filtered_sales["CustomerID"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Total Customers", f"{total_customers:,}")
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

    st.divider()

    # --- Revenue Trend ---
    monthly = (
        filtered_sales.groupby(
            filtered_sales["OrderDate"].dt.to_period("M")
        )["LineTotal"]
        .sum()
        .reset_index()
    )
    monthly["OrderDate"] = monthly["OrderDate"].dt.to_timestamp()

    fig_trend = px.line(
        monthly,
        x="OrderDate",
        y="LineTotal",
        title="Revenue Trend Over Time",
        labels={"OrderDate": "Month", "LineTotal": "Revenue"},
    )
    fig_trend.update_traces(line_width=2.5)
    st.plotly_chart(fig_trend, width='stretch')

    st.divider()

    # --- Category and Territory Charts ---
    col_left, col_right = st.columns(2)

    with col_left:
        category_rev = (
            filtered_sales.groupby("Category")["LineTotal"]
            .sum()
            .reset_index()
            .sort_values("LineTotal", ascending=True)
        )
        fig_cat = px.bar(
            category_rev,
            x="LineTotal",
            y="Category",
            orientation="h",
            title="Revenue by Category",
            labels={"LineTotal": "Revenue", "Category": "Category"},
        )
        st.plotly_chart(fig_cat, width='stretch')

    with col_right:
        territory_rev = (
            filtered_sales.groupby("Territory")["LineTotal"]
            .sum()
            .reset_index()
            .sort_values("LineTotal", ascending=True)
        )
        fig_terr = px.bar(
            territory_rev,
            x="LineTotal",
            y="Territory",
            orientation="h",
            title="Revenue by Territory",
            labels={"LineTotal": "Revenue", "Territory": "Territory"},
        )
        st.plotly_chart(fig_terr, width='stretch')

elif page == "Customer Analysis":
    st.title("👥 Customer Analysis")

    # --- Segment Filter ---
    segments = sorted(rfm["CustomerSegment"].unique())
    selected_segments = st.multiselect(
        "Filter by Segment", segments, default=segments
    )
    filtered_rfm = rfm[rfm["CustomerSegment"].isin(selected_segments)]
    filtered_customers = customers[
        customers["CustomerID"].isin(filtered_rfm["CustomerID"])
    ]

    st.divider()

    # --- KPI Cards ---
    total_customers = filtered_rfm["CustomerID"].nunique()
    avg_revenue = filtered_customers["TotalRevenue"].mean()
    pct_of_total = total_customers / rfm["CustomerID"].nunique() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Avg Revenue per Customer", f"${avg_revenue:,.2f}")
    col3.metric("% of Total Customers", f"{pct_of_total:.1f}%")

    st.divider()

    # --- Donut Chart and Revenue by Segment ---
    col_left, col_right = st.columns(2)

    with col_left:
        segment_counts = (
            filtered_rfm.groupby("CustomerSegment")["CustomerID"]
            .nunique()
            .reset_index()
        )
        segment_counts.columns = ["CustomerSegment", "CustomerCount"]
        fig_donut = px.pie(
            segment_counts,
            names="CustomerSegment",
            values="CustomerCount",
            title="Customer Segments",
            hole=0.4
        )
        st.plotly_chart(fig_donut, width='stretch')

    with col_right:
        segment_rev = (
            filtered_customers.merge(
                filtered_rfm[["CustomerID", "CustomerSegment"]],
                on="CustomerID"
            )
            .groupby("CustomerSegment")["TotalRevenue"]
            .sum()
            .reset_index()
            .sort_values("TotalRevenue", ascending=True)
        )
        fig_seg_rev = px.bar(
            segment_rev,
            x="TotalRevenue",
            y="CustomerSegment",
            orientation="h",
            title="Revenue by Customer Segment",
            labels={
                "TotalRevenue": "Revenue",
                "CustomerSegment": "Segment"
            }
        )
        st.plotly_chart(fig_seg_rev, width='stretch')

    st.divider()

    # --- Revenue Distribution ---
    bins = [0, 1000, 5000, 10000, 50000, 100000, float("inf")]
    labels = ["< $1K", "$1K-$5K", "$5K-$10K", "$10K-$50K", "$50K-$100K", "> $100K"]
    filtered_customers = filtered_customers.copy()
    filtered_customers["RevenueBucket"] = pd.cut(
        filtered_customers["TotalRevenue"],
        bins=bins,
        labels=labels
    )
    bucket_counts = (
        filtered_customers.groupby("RevenueBucket", observed=True)["CustomerID"]
        .nunique()
        .reset_index()
    )
    bucket_counts.columns = ["RevenueBucket", "CustomerCount"]
    fig_dist = px.bar(
        bucket_counts,
        x="RevenueBucket",
        y="CustomerCount",
        title="Customer Revenue Distribution",
        labels={
            "RevenueBucket": "Revenue Range",
            "CustomerCount": "Number of Customers"
        },
        text="CustomerCount"
    )
    fig_dist.update_traces(textposition="outside")
    st.plotly_chart(fig_dist, width='stretch')

elif page == "Product Analysis":
    st.title("🛍️ Product Analysis")

    # --- Filters ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        years = sorted(sales["OrderDate"].dt.year.unique())
        selected_years = st.multiselect(
            "Filter by Year", years, default=years
        )
    with col_f2:
        categories = sorted(sales["Category"].unique())
        selected_categories = st.multiselect(
            "Filter by Category", categories, default=categories
        )

    filtered_sales = sales[
        (sales["OrderDate"].dt.year.isin(selected_years)) &
        (sales["Category"].isin(selected_categories))
    ]

    st.divider()

    # --- Top 10 Products ---
    top_products = (
        filtered_sales.groupby("ProductName")["LineTotal"]
        .sum()
        .reset_index()
        .sort_values("LineTotal", ascending=False)
        .head(10)
        .sort_values("LineTotal", ascending=True)
    )
    fig_products = px.bar(
        top_products,
        x="LineTotal",
        y="ProductName",
        orientation="h",
        title="Top 10 Products by Revenue",
        labels={"LineTotal": "Revenue", "ProductName": "Product"},
        text="LineTotal"
    )
    fig_products.update_traces(
        texttemplate="%{text:$,.0f}",
        textposition="outside"
    )
    st.plotly_chart(fig_products, width='stretch')

    st.divider()

    # --- Subcategory Treemap and Category Over Time ---
    col_left, col_right = st.columns(2)

    with col_left:
        subcat_rev = (
            filtered_sales.groupby(["Category", "Subcategory"])["LineTotal"]
            .sum()
            .reset_index()
        )
        fig_treemap = px.treemap(
            subcat_rev,
            path=["Category", "Subcategory"],
            values="LineTotal",
            title="Revenue by Subcategory",
            labels={"LineTotal": "Revenue"}
        )
        st.plotly_chart(fig_treemap, width='stretch')

    with col_right:
        cat_year = (
            filtered_sales.groupby(
                [filtered_sales["OrderDate"].dt.year, "Category"]
            )["LineTotal"]
            .sum()
            .reset_index()
        )
        cat_year.columns = ["Year", "Category", "Revenue"]
        fig_cat_year = px.bar(
            cat_year,
            x="Year",
            y="Revenue",
            color="Category",
            barmode="group",
            title="Revenue by Category Over Time",
            labels={"Revenue": "Revenue", "Year": "Year"}
        )
        st.plotly_chart(fig_cat_year, width='stretch')

    st.divider()

    # --- Top 10 Customers Table ---
    st.subheader("Top 10 Customers by Revenue")
    top_customers = (
        customers.merge(
            rfm[["CustomerID", "CustomerSegment"]],
            on="CustomerID"
        )
        .sort_values("TotalRevenue", ascending=False)
        .head(10)
        [["CustomerID", "TotalOrders", "TotalRevenue", "CustomerSegment"]]
        .reset_index(drop=True)
    )
    top_customers.index += 1
    top_customers["TotalRevenue"] = top_customers["TotalRevenue"].apply(
        lambda x: f"${x:,.2f}"
    )
    st.dataframe(top_customers, width='stretch')