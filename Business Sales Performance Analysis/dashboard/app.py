import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration for a premium dashboard feel
st.set_page_config(
    page_title="Business Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism and modern dark design
st.markdown("""
<style>
    /* Main Background and Text */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Header customization */
    .main-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px !important;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Card Container */
    div[data-testid="metric-container"] {
        background: rgba(22, 28, 45, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Modify streamlit default container padding */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Error loading sales_data.csv. Please verify the dataset has been generated in data/sales_data.csv.")
    st.stop()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.image("https://img.icons8.com/color/96/000000/dashboard.png", width=80)
st.sidebar.markdown("<h2 style='color:#f3f4f6;'>Dashboard Filters</h2>", unsafe_allow_html=True)

# 1. Date range filter
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 2. Region filter
all_regions = sorted(df['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Select Regions", all_regions, default=all_regions)

# 3. Category filter
all_categories = sorted(df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Select Categories", all_categories, default=all_categories)

# 4. Customer Segment filter
all_segments = sorted(df['Customer Segment'].unique().tolist())
selected_segments = st.sidebar.multiselect("Select Customer Segments", all_segments, default=all_segments)

# Apply filters
filtered_df = df[
    (df['Order Date'].dt.date >= start_date) & 
    (df['Order Date'].dt.date <= end_date) &
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['Customer Segment'].isin(selected_segments))
]

# ----------------- HEADER -----------------
st.markdown("<h1 class='main-title'>Business Sales Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interactive KPI metrics and visual analysis of retail sales transactions</p>", unsafe_allow_html=True)

# ----------------- KPI CARDS -----------------
total_sales = filtered_df['Sales Revenue'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df['Order ID'].nunique()
avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.metric("Total Revenue", f"₹{total_sales:,.2f}")
with kpi_col2:
    st.metric("Total Profit", f"₹{total_profit:,.2f}", delta=f"{(total_profit/total_sales*100):.1f}% Margin" if total_sales > 0 else "0%")
with kpi_col3:
    st.metric("Net Profit Margin", f"{profit_margin:.2f}%")
with kpi_col4:
    st.metric("Total Unique Orders", f"{total_orders:,}", delta=f"AOV: ₹{avg_order_value:.2f}")

st.markdown("---")

# ----------------- VISUALIZATIONS -----------------

# Row 1: Monthly Trends & Region Share
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Monthly Sales and Profit Trends")
    # Group by month
    monthly_data = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M')).agg(
        Sales_Revenue=('Sales Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    monthly_data['Month'] = monthly_data['Order Date'].astype(str)
    
    # Plotly combination line chart
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Bar(
        x=monthly_data['Month'],
        y=monthly_data['Sales_Revenue'],
        name='Revenue',
        marker_color='#3b82f6',
        opacity=0.8
    ))
    fig_trends.add_trace(go.Scatter(
        x=monthly_data['Month'],
        y=monthly_data['Profit'],
        name='Profit',
        yaxis='y2',
        line=dict(color='#10b981', width=3, shape='spline'),
        mode='lines+markers'
    ))
    
    fig_trends.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title=dict(text='Revenue (₹)', font=dict(color='#3b82f6')), tickfont=dict(color='#3b82f6')),
        yaxis2=dict(title=dict(text='Profit (₹)', font=dict(color='#10b981')), tickfont=dict(color='#10b981'), anchor='x', overlaying='y', side='right'),
        margin=dict(l=20, r=20, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trends, use_container_width=True)

with col2:
    st.markdown("### Sales by Region")
    region_sales = filtered_df.groupby('Region')['Sales Revenue'].sum().reset_index()
    
    fig_region = px.pie(
        region_sales, 
        values='Sales Revenue', 
        names='Region', 
        hole=0.45,
        color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
    )
    fig_region.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Row 2: Category Breakdown & Top Products
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Sales and Profit by Category")
    cat_data = filtered_df.groupby('Category').agg(
        Sales_Revenue=('Sales Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    
    fig_cat = go.Figure(data=[
        go.Bar(name='Revenue', x=cat_data['Category'], y=cat_data['Sales_Revenue'], marker_color='#3b82f6', marker=dict(cornerradius=4)),
        go.Bar(name='Profit', x=cat_data['Category'], y=cat_data['Profit'], marker_color='#10b981', marker=dict(cornerradius=4))
    ])
    fig_cat.update_layout(
        barmode='group',
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col4:
    st.markdown("### Top 10 Products by Sales")
    top_products = filtered_df.groupby('Product Name')['Sales Revenue'].sum().reset_index()
    top_products = top_products.sort_values(by='Sales Revenue', ascending=True).tail(10)
    
    # Trim product names for readability
    top_products['Prod_Short'] = top_products['Product Name'].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)
    
    fig_products = px.bar(
        top_products,
        x='Sales Revenue',
        y='Prod_Short',
        orientation='h',
        color_discrete_sequence=['#8b5cf6']
    )
    fig_products.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_title="Sales Revenue (₹)",
        yaxis_title=""
    )
    st.plotly_chart(fig_products, use_container_width=True)

# Row 3: Detail Data Table & Subcategory Analysis
st.markdown("### Sub-Category Performance breakdown")
subcat_data = filtered_df.groupby(['Category', 'Sub-Category']).agg(
    Sales_Revenue=('Sales Revenue', 'sum'),
    Quantity_Sold=('Quantity Sold', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()
subcat_data['Profit_Margin'] = (subcat_data['Profit'] / subcat_data['Sales_Revenue'] * 100).round(2)
subcat_data = subcat_data.sort_values(by='Sales_Revenue', ascending=False)

# Format columns
styled_subcat = subcat_data.copy()
styled_subcat['Sales_Revenue'] = styled_subcat['Sales_Revenue'].apply(lambda x: f"₹{x:,.2f}")
styled_subcat['Profit'] = styled_subcat['Profit'].apply(lambda x: f"₹{x:,.2f}")
styled_subcat['Profit_Margin'] = styled_subcat['Profit_Margin'].apply(lambda x: f"{x:.2f}%")

st.dataframe(styled_subcat, use_container_width=True, hide_index=True)
