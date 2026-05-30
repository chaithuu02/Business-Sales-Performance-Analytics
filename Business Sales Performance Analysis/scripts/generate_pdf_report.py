import os
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

class SalesReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Don't show header on cover page (Page 1)
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(107, 114, 128) # Gray-500
            self.cell(0, 5, 'Business Sales Performance Analytics Report', border=0, ln=0, align='L')
            self.cell(0, 5, datetime.now().strftime("%B %Y"), border=0, ln=1, align='R')
            # Thin divider line
            self.set_draw_color(229, 231, 235) # Gray-200
            self.line(15, 22, 195, 22)
            self.ln(5)
            
    def footer(self):
        self.set_y(-15)
        # Thin line above footer
        self.set_draw_color(229, 231, 235)
        self.line(15, 282, 195, 282)
        
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(107, 114, 128)
        self.cell(0, 10, 'CONFIDENTIAL - FUTURE RETAIL CORP', border=0, ln=0, align='L')
        self.cell(0, 10, f'Page {self.page_no()}', border=0, ln=0, align='R')

def build_pdf_report():
    print("Beginning PDF Report generation...")
    
    # Load dataset to extract KPIs for the report
    df = pd.read_csv("data/sales_data.csv")
    total_sales = df['Sales Revenue'].sum()
    total_profit = df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100
    total_orders = df['Order ID'].nunique()
    avg_order_value = total_sales / total_orders
    
    # Calculate yearly stats
    df['Year'] = pd.to_datetime(df['Order Date']).dt.year
    yearly_sales = df.groupby('Year')['Sales Revenue'].sum()
    yearly_growth = yearly_sales.pct_change() * 100
    
    pdf = SalesReportPDF()
    
    # ----------------------------------------------------
    # PAGE 1: COVER PAGE
    # ----------------------------------------------------
    pdf.add_page()
    
    # Large colored decorative top block (Deep Corporate Blue)
    pdf.set_fill_color(30, 58, 138) # Navy #1E3A8A
    pdf.rect(0, 0, 210, 100, 'F')
    
    pdf.ln(25)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, 'BUSINESS SALES', ln=1, align='L')
    pdf.cell(0, 12, 'PERFORMANCE REPORT', ln=1, align='L')
    
    pdf.ln(5)
    # Accent color line (Gold/Amber)
    pdf.set_draw_color(245, 158, 11) # Gold #F59E0B
    pdf.set_line_width(2)
    pdf.line(15, 68, 80, 68)
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(229, 231, 235)
    pdf.cell(0, 8, 'A Comprehensive Data-Driven Sales & Profitability Analysis', ln=1)
    
    # White background area content
    pdf.set_y(120)
    pdf.set_text_color(31, 41, 55) # Gray-800
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Executive Report Overview', ln=1)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(75, 85, 99) # Gray-600
    overview_text = (
        "This performance report analyzes transactions over the last four fiscal years (2022 - 2025). "
        "Through extensive data preparation and exploratory data analysis (EDA), this report isolates "
        "key growth opportunities, evaluates regional disparities, categorizes product success lines, "
        "and outlines actionable strategies to maximize overall profitability."
    )
    pdf.multi_cell(0, 6, overview_text)
    
    # Metadata footer block
    pdf.set_y(220)
    pdf.set_draw_color(229, 231, 235)
    pdf.set_line_width(0.5)
    pdf.line(15, 215, 195, 215)
    
    pdf.set_text_color(107, 114, 128)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(45, 6, 'PREPARED FOR:', ln=0)
    pdf.cell(60, 6, 'PREPARED BY:', ln=0)
    pdf.cell(45, 6, 'DATE OF ISSUE:', ln=1)
    
    pdf.set_text_color(31, 41, 55)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(45, 6, 'Corporate Executive Board', ln=0)
    pdf.cell(60, 6, 'Data Science Division', ln=0)
    pdf.cell(45, 6, datetime.now().strftime("%B %d, %Y"), ln=1)
    
    # ----------------------------------------------------
    # PAGE 2: EXECUTIVE SUMMARY & KPIs
    # ----------------------------------------------------
    pdf.add_page()
    pdf.ln(10)
    
    # Section Header
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, '1. Executive Summary & KPIs', ln=1)
    pdf.ln(2)
    
    pdf.set_text_color(75, 85, 99)
    pdf.set_font('Helvetica', '', 11)
    summary_p1 = (
        "Our sales operations generated significant volumes between 2022 and 2025. "
        "A critical review of the core metrics reveals a healthy net margin, but also highlights "
        "clear areas where operational changes are required. Below are the key performance indicators "
        "that summarize the cumulative performance across all segments and regions:"
    )
    pdf.multi_cell(0, 6, summary_p1)
    pdf.ln(5)
    
    # KPI Table
    pdf.set_fill_color(30, 58, 138)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(90, 8, ' Key Performance Indicator', border=1, fill=True)
    pdf.cell(90, 8, ' Value', border=1, fill=True, align='R')
    pdf.ln(8)
    
    pdf.set_text_color(31, 41, 55)
    pdf.set_font('Helvetica', '', 10)
    
    kpis = [
        ("Total Sales Revenue", f"Rs. {total_sales:,.2f}"),
        ("Total Profit Generated", f"Rs. {total_profit:,.2f}"),
        ("Overall Profit Margin (%)", f"{profit_margin:.2f}%"),
        ("Total Unique Transactions (Orders)", f"{total_orders:,}"),
        ("Average Order Value (AOV)", f"Rs. {avg_order_value:,.2f}")
    ]
    
    for label, val in kpis:
        pdf.cell(90, 8, f"  {label}", border=1)
        pdf.cell(90, 8, f"  {val}", border=1, align='R')
        pdf.ln(8)
        
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(75, 85, 99)
    summary_p2 = (
        "Analyzing year-over-year progress, we note a steady upward trajectory in transaction volume. "
        "However, growth rates vary between product categories. Our primary objective is to shift focus "
        "toward high-margin product lines while resolving shipping and marketing inefficiencies in underperforming units."
    )
    pdf.multi_cell(0, 6, summary_p2)
    pdf.ln(8)
    
    # Yearly Growth Table
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 8, 'Year-over-Year Growth Performance', ln=1)
    pdf.ln(2)
    
    pdf.set_fill_color(243, 244, 246) # Light gray
    pdf.set_text_color(31, 41, 55)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(60, 8, ' Year', border=1, fill=True)
    pdf.cell(60, 8, ' Sales Revenue', border=1, fill=True, align='R')
    pdf.cell(60, 8, ' Growth Rate (YoY)', border=1, fill=True, align='R')
    pdf.ln(8)
    
    pdf.set_font('Helvetica', '', 10)
    for yr in sorted(yearly_sales.index):
        sales = yearly_sales[yr]
        growth = yearly_growth.get(yr, np.nan)
        growth_str = f"{growth:+.2f}%" if not pd.isna(growth) else "Baseline"
        
        pdf.cell(60, 8, f"  {yr}", border=1)
        pdf.cell(60, 8, f"  Rs. {sales:,.2f}", border=1, align='R')
        pdf.cell(60, 8, f"  {growth_str}", border=1, align='R')
        pdf.ln(8)
        
    # ----------------------------------------------------
    # PAGE 3: SALES TREND & REGIONAL ANALYSIS
    # ----------------------------------------------------
    pdf.add_page()
    pdf.ln(10)
    
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, '2. Monthly Sales & Regional Performance', ln=1)
    pdf.ln(2)
    
    pdf.set_text_color(75, 85, 99)
    pdf.set_font('Helvetica', '', 11)
    trend_desc = (
        "The line chart below tracks monthly revenue and profit. We observe clear seasonality, "
        "with major spikes in sales volume during November and December. This corresponds with "
        "retail holiday trends and commercial year-end purchases."
    )
    pdf.multi_cell(0, 6, trend_desc)
    pdf.ln(4)
    
    # Embed Monthly Trends Image
    if os.path.exists("images/monthly_trends.png"):
        pdf.image("images/monthly_trends.png", x=15, w=180, h=75)
        pdf.ln(5)
        
    region_desc = (
        "On a regional basis, the West region generates the highest revenue, followed closely by the East. "
        "However, the Central region exhibits a significantly lower profit margin despite moderate sales. "
        "This indicates a need to review pricing strategies and logistics costs in Central states."
    )
    pdf.multi_cell(0, 6, region_desc)
    pdf.ln(4)
    
    # Embed Regional Performance Image
    if os.path.exists("images/regional_performance.png"):
        pdf.image("images/regional_performance.png", x=15, w=180, h=75)
        
    # ----------------------------------------------------
    # PAGE 4: CATEGORY & PRODUCT PERFORMANCE
    # ----------------------------------------------------
    pdf.add_page()
    pdf.ln(10)
    
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, '3. Product Category & Profitability Factors', ln=1)
    pdf.ln(2)
    
    pdf.set_text_color(75, 85, 99)
    pdf.set_font('Helvetica', '', 11)
    category_desc = (
        "Technology remains our primary profit driver, yielding high margins across phones and copiers. "
        "Office Supplies show stable performance and low overhead, while Furniture generates the lowest profit margins. "
        "Tables and bookcases consistently lose money due to high shipping costs and aggressive discounting."
    )
    pdf.multi_cell(0, 6, category_desc)
    pdf.ln(4)
    
    # Embed Category Analysis Image
    if os.path.exists("images/category_analysis.png"):
        pdf.image("images/category_analysis.png", x=15, w=180, h=75)
        pdf.ln(5)
        
    product_desc = (
        "Our top products by sales consist of high-value Technology and Furniture items. "
        "Conversely, our bottom 10 products represent significant loss leaders. Reviewing pricing models "
        "and supplier agreements for these unprofitable items is a key priority."
    )
    pdf.multi_cell(0, 6, product_desc)
    pdf.ln(4)
    
    # Embed Product Performance Image
    if os.path.exists("images/product_performance.png"):
        pdf.image("images/product_performance.png", x=15, w=180, h=75)
        
    # ----------------------------------------------------
    # PAGE 5: STRATEGIC BUSINESS RECOMMENDATIONS
    # ----------------------------------------------------
    pdf.add_page()
    pdf.ln(10)
    
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, '4. Actionable Business Recommendations', ln=1)
    pdf.ln(4)
    
    # Recommendation blocks with distinct spacing and styles
    recommendations = [
        ("1. Target Marketing in High-Performing Regions", 
         "Double down on marketing campaigns in the West and East regions. Since these regions exhibit "
         "both high sales volume and healthy profit margins, incremental advertising investments will yield a "
         "higher return on ad spend (ROAS)."),
         
        ("2. Rationalize the Furniture Category & Shipping Policy", 
         "Address losses in the Furniture category (especially Tables) by adjusting shipping policies. "
         "Implement a freight shipping surcharge for bulky items instead of offering standard free shipping, "
         "and renegotiate delivery rates with logistics partners."),
         
        ("3. Optimize Inventory for Top Technology Products", 
         "Ensure consistent inventory levels for top-performing technology products like copiers and smartphones. "
         "Establish automated reorder thresholds with manufacturers to avoid stockouts during Q4 peak seasons."),
         
        ("4. Re-evaluate Pricing and Discounting Thresholds", 
         "Limit maximum promotional discounts on low-margin subcategories. Data reveals that discounts exceeding "
         "20% convert transactions into net-loss sales. Implement system-level approvals for higher discounts."),
         
        ("5. Focus on Customer Lifetime Value (CLV) in Corporate Segment", 
         "Expand loyalty programs and bulk-purchase incentives for the Corporate and Home Office segments. "
         "These segments tend to place larger average orders, helping amortize fixed customer acquisition and delivery costs.")
    ]
    
    for title, desc in recommendations:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 6, title, ln=1)
        pdf.ln(1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(6)
        
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, 'Conclusion', ln=1)
    pdf.ln(1)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(75, 85, 99)
    conclusion_text = (
        "By focusing on margins rather than sales volume alone, Future Retail Corp can significantly increase "
        "profitability. Addressing bulky item logistics, managing promotional discounts, and expanding the "
        "high-performing Technology lines will lay the foundation for sustainable financial growth."
    )
    pdf.multi_cell(0, 5, conclusion_text)
    
    # Save Report
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/Business_Sales_Performance_Report.pdf"
    pdf.output(report_path)
    print(f"Successfully generated report at: {report_path}")

if __name__ == "__main__":
    build_pdf_report()
