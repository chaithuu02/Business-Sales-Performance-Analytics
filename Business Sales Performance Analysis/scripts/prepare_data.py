import os
import urllib.request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def download_dataset():
    """
    Tries to download the Superstore dataset from multiple reliable raw GitHub URLs.
    Returns a pandas DataFrame if successful, else None.
    """
    urls = [
        "https://raw.githubusercontent.com/Vamshi-Kalyan/Data-Analytics-Projects/master/Sample%20-%20Superstore.csv",
        "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/Sample%20-%20Superstore.csv",
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv" # Just fallback to check URL fetch
    ]
    
    encodings = ["utf-8", "cp1252", "latin1"]
    
    for url in urls:
        print(f"Attempting to download dataset from: {url}")
        for encoding in encodings:
            try:
                # Use a custom User-Agent to avoid blocking
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    df = pd.read_csv(response, encoding=encoding)
                
                # Verify this is the Superstore dataset (must have columns like Category, Sales, Profit, etc.)
                if 'Category' in df.columns and 'Sales' in df.columns:
                    print(f"Successfully downloaded and loaded dataset with encoding '{encoding}'!")
                    return df
            except Exception as e:
                continue
    return None

def generate_synthetic_data(num_rows=8000):
    """
    Generates a high-quality, realistic Superstore-like dataset.
    This serves as a robust fallback in case of no internet access.
    """
    print(f"Generating {num_rows} rows of highly realistic synthetic sales data...")
    np.random.seed(42)
    
    # Categories and subcategories
    categories = {
        'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Art', 'Storage', 'Appliances', 'Fasteners', 'Envelopes', 'Labels']
    }
    
    # Products within subcategories
    products = {
        'Phones': ['iPhone 15 Pro', 'Samsung Galaxy S24', 'Google Pixel 8', 'OnePlus 12', 'Nokia retro phone'],
        'Accessories': ['Logitech Wireless Mouse', 'Mechanical Keyboard', 'USB-C Hub', 'Noise Cancelling Headphones', 'Leather Laptop Sleeve'],
        'Copiers': ['Canon ImageClass Copier', 'HP LaserJet Pro Copier', 'Brother Monochrome Copier', 'Xerox WorkCentre'],
        'Machines': ['3D Printer Pro', 'Label Printer XL', 'Heavy Duty Shredder', 'Scanner & Document Digitizer'],
        'Chairs': ['Ergonomic Office Chair', 'Executive Leather Chair', 'Mesh Task Chair', 'Folding Chair 4-Pack'],
        'Tables': ['Standing Desk Wood', 'Conference Room Table', 'Coffee Table Modern', 'Drafting Table Adjustable'],
        'Bookcases': ['5-Shelf Oak Bookcase', '3-Shelf Walnut Bookcase', 'Metal Frame Bookshelf', 'Corner Bookshelf White'],
        'Furnishings': ['LED Desk Lamp', 'Anti-Fatigue Floor Mat', 'Desk Organizer Tray', 'Wall Clock Brushed Nickel'],
        'Paper': ['Premium Copy Paper Letter', 'Colored Cardstock', 'Recycled Printer Paper', 'Photo Paper Glossy'],
        'Binders': ['3-Ring Binder 2-inch', 'Heavy Duty D-Ring Binder', 'Clear View Binder', 'Zipper Binder Portfolio'],
        'Art': ['Sketching Colored Pencils', 'Whiteboard Markers 12-Pack', 'Acrylic Paint Set', 'Fine Tip Fineliners'],
        'Storage': ['Plastic Storage Bins 6-Pack', 'File Filing Cabinet 3-Drawer', 'Under-bed Storage Organizer', 'Heavy Duty Shelving Unit'],
        'Appliances': ['Compact Office Refrigerator', 'Microwave Oven Stainless Steel', 'Keurig Coffee Maker', 'Air Purifier HEPA'],
        'Fasteners': ['Standard Staples Box', 'Paper Clips Jumbo', 'Rubber Bands Asst.', 'Push Pins Assorted'],
        'Envelopes': ['Catalog Envelopes 100-Count', 'Security Tint Self-Seal Envelopes', 'Bubble Mailers Padded'],
        'Labels': ['Address Labels Roll', 'File Folder Labels', 'Shipping Labels Laser']
    }
    
    # Customers segments
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    # Regions and states/cities
    regions = {
        'East': [('New York', 'New York City'), ('Massachusetts', 'Boston'), ('Pennsylvania', 'Philadelphia'), ('District of Columbia', 'Washington')],
        'West': [('California', 'Los Angeles'), ('California', 'San Francisco'), ('Washington', 'Seattle'), ('Oregon', 'Portland')],
        'Central': [('Illinois', 'Chicago'), ('Texas', 'Houston'), ('Texas', 'Austin'), ('Michigan', 'Detroit')],
        'South': [('Florida', 'Miami'), ('Georgia', 'Atlanta'), ('North Carolina', 'Charlotte'), ('Tennessee', 'Nashville')]
    }
    
    # Date generation over 4 years (2022 to 2025)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range = (end_date - start_date).days
    
    data = []
    
    for i in range(1, num_rows + 1):
        order_id = f"CA-{start_date.year + np.random.randint(0, 4)}-{100000 + i}"
        
        # Generate date with seasonal patterns (more sales in Q4: Nov/Dec)
        day_offset = np.random.randint(0, date_range)
        order_date = start_date + timedelta(days=day_offset)
        # Seasonal multiplier: boost probabilities in Nov (month 11) and Dec (month 12)
        if order_date.month not in [11, 12] and np.random.rand() > 0.7:
            # Shift some random dates to Nov/Dec to simulate seasonality
            target_month = np.random.choice([11, 12])
            if target_month == 11 and order_date.day == 31:
                order_date = order_date.replace(month=11, day=30)
            else:
                order_date = order_date.replace(month=target_month)
            
        segment = np.random.choice(segments, p=[0.5, 0.3, 0.2])
        
        region = np.random.choice(list(regions.keys()))
        state_city_info = regions[region][np.random.randint(len(regions[region]))]
        state, city = state_city_info[0], state_city_info[1]
        
        cat = np.random.choice(list(categories.keys()), p=[0.3, 0.3, 0.4])
        sub_cat = np.random.choice(categories[cat])
        prod_name = np.random.choice(products[sub_cat])
        
        # Quantity
        quantity = int(np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=[0.25, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.04, 0.03, 0.03]))
        
        # Base pricing and costs by subcategory
        price_lookup = {
            'Phones': (150.0, 900.0, 0.15),      # min_price, max_price, profit_margin_avg
            'Accessories': (15.0, 150.0, 0.25),
            'Copiers': (800.0, 3000.0, 0.35),
            'Machines': (200.0, 1500.0, 0.05), # low margin
            'Chairs': (80.0, 450.0, 0.12),
            'Tables': (150.0, 800.0, -0.05),    # tables are often sold at a loss
            'Bookcases': (100.0, 600.0, 0.08),
            'Furnishings': (10.0, 120.0, 0.20),
            'Paper': (5.0, 40.0, 0.40),
            'Binders': (2.0, 30.0, 0.45),
            'Art': (3.0, 50.0, 0.30),
            'Storage': (20.0, 250.0, 0.15),
            'Appliances': (50.0, 500.0, 0.18),
            'Fasteners': (1.0, 15.0, 0.35),
            'Envelopes': (5.0, 25.0, 0.40),
            'Labels': (2.0, 20.0, 0.40)
        }
        
        min_p, max_p, avg_margin = price_lookup[sub_cat]
        unit_price = np.random.uniform(min_p, max_p)
        
        # Calculate revenue (sales)
        sales = round(unit_price * quantity, 2)
        
        # Profit margin has some variance, maybe discount impact
        discount_applied = np.random.choice([0.0, 0.1, 0.15, 0.2, 0.3, 0.5], p=[0.5, 0.15, 0.1, 0.1, 0.1, 0.05])
        
        # Net sales after discount
        discount_value = sales * discount_applied
        sales_revenue = round(sales - discount_value, 2)
        
        # Calculate cost based on target margin (before discount)
        cost_price = unit_price * (1 - avg_margin)
        total_cost = cost_price * quantity
        
        # Profit is revenue minus total cost
        profit = round(sales_revenue - total_cost, 2)
        
        # Keep track of records
        data.append({
            "Row ID": i,
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Customer Segment": segment,
            "Region": region,
            "State": state,
            "City": city,
            "Category": cat,
            "Sub-Category": sub_cat,
            "Product Name": prod_name,
            "Sales": sales_revenue,
            "Quantity": quantity,
            "Discount": discount_applied,
            "Profit": profit
        })
        
    return pd.DataFrame(data)

def clean_and_validate_data(df):
    """
    Cleans and validates the dataset:
    - Standardize column names and formats
    - Handle missing values
    - Remove duplicates
    - Validate numerical columns
    - Format dates
    """
    print("Beginning data cleaning and validation process...")
    
    # 1. Handle Column Names Mapping
    # Standard superstore columns to target columns:
    # 'Order ID', 'Order Date', 'Product Name', 'Category', 'Sub-Category', 'Sales', 'Quantity', 'Profit', 'Customer Segment', 'Region', 'State', 'City'
    rename_dict = {
        'Sales': 'Sales Revenue',
        'Quantity': 'Quantity Sold',
        'State': 'State/City' # We will combine or rename
    }
    
    # If the standard dataset contains State and City separately, let's create a combined 'State/City' field
    if 'State' in df.columns and 'City' in df.columns:
        df['State/City'] = df['State'] + ", " + df['City']
        if 'State' in rename_dict:
            del rename_dict['State']
        
    df = df.rename(columns=rename_dict)
    
    # Select only required columns (or keep additional ones if needed, but ensure required are present)
    required_cols = [
        'Order ID', 'Order Date', 'Product Name', 'Category', 'Sub-Category', 
        'Sales Revenue', 'Quantity Sold', 'Profit', 'Customer Segment', 'Region', 'State/City'
    ]
    
    # In case any column was missing from original source, add standard fallbacks
    for col in required_cols:
        if col not in df.columns:
            if col == 'Customer Segment' and 'Segment' in df.columns:
                df['Customer Segment'] = df['Segment']
            elif col == 'Sales Revenue' and 'Sales' in df.columns:
                df['Sales Revenue'] = df['Sales']
            elif col == 'Quantity Sold' and 'Quantity' in df.columns:
                df['Quantity Sold'] = df['Quantity']
            else:
                df[col] = np.nan
                
    df = df[required_cols]
    
    # 2. Handle missing values
    initial_rows = len(df)
    
    # Fill categorical missing values with a default string
    categorical_cols = ['Product Name', 'Category', 'Sub-Category', 'Customer Segment', 'Region', 'State/City']
    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
        
    # Numerical missing values - drop or impute
    # If Sales Revenue or Quantity Sold is null, we can fill with reasonable default or drop
    df['Sales Revenue'] = pd.to_numeric(df['Sales Revenue'], errors='coerce')
    df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    
    # Drop rows with null Sales or Quantity (critical columns)
    df = df.dropna(subset=['Sales Revenue', 'Quantity Sold'])
    
    # For Profit, if missing, we can estimate from Sales based on average sub-category margin
    if df['Profit'].isnull().any():
        print("Handling missing Profit values...")
        # Simple estimate: Profit is 15% of Sales Revenue if null
        df['Profit'] = df['Profit'].fillna(df['Sales Revenue'] * 0.15)
        
    # 3. Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate rows.")
        
    # 4. Standardize text formats
    # Capitalize categories and regions
    df['Category'] = df['Category'].str.title()
    df['Sub-Category'] = df['Sub-Category'].str.title()
    df['Customer Segment'] = df['Customer Segment'].str.title()
    df['Region'] = df['Region'].str.title()
    
    # 5. Validate numerical columns
    # Sales Revenue must be positive
    df['Sales Revenue'] = df['Sales Revenue'].apply(lambda x: max(0.01, x))
    # Quantity Sold must be an integer >= 1
    df['Quantity Sold'] = df['Quantity Sold'].apply(lambda x: max(1, int(round(x))))
    
    # Convert USD to INR (1 USD = 83 INR)
    print("Converting currency from USD ($) to INR at a rate of 1 USD = 83 INR...")
    df['Sales Revenue'] = df['Sales Revenue'] * 83.0
    df['Profit'] = df['Profit'] * 83.0
    
    # Profit must be rounded
    df['Profit'] = df['Profit'].round(2)
    df['Sales Revenue'] = df['Sales Revenue'].round(2)
    
    # 6. Convert and validate date format
    # Try parsing dates with common formats
    parsed_dates = []
    for date_str in df['Order Date']:
        parsed_date = None
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%d-%b-%Y'):
            try:
                parsed_date = datetime.strptime(str(date_str).strip(), fmt)
                break
            except ValueError:
                continue
        if parsed_date is None:
            # Fallback to current date or standard offset if unparseable
            parsed_date = datetime(2025, 1, 1)
        parsed_dates.append(parsed_date)
        
    df['Order Date'] = [d.strftime("%Y-%m-%d") for d in parsed_dates]
    
    # Sort by date for logical progression
    df = df.sort_values(by='Order Date').reset_index(drop=True)
    
    print(f"Data cleaning complete! Final shape: {df.shape}")
    return df

def main():
    # Make directories if they don't exist
    os.makedirs("data", exist_ok=True)
    
    # Try downloading first
    df = download_dataset()
    
    # If downloading failed or is incomplete, use high-quality synthetic data
    if df is None:
        print("Could not download external dataset. Reverting to synthetic data generator.")
        df = generate_synthetic_data(num_rows=8000)
    else:
        # Save a copy of raw data for completeness
        df.to_csv("data/sales_data_raw.csv", index=False)
        print("Saved raw dataset to data/sales_data_raw.csv")
        
    # Clean and validate the data
    cleaned_df = clean_and_validate_data(df)
    
    # Save cleaned data
    cleaned_df.to_csv("data/sales_data.csv", index=False)
    print("Successfully saved cleaned dataset to data/sales_data.csv")

if __name__ == "__main__":
    main()
