import os
import pandas as pd
import json

def main():
    csv_path = "data/sales_data.csv"
    js_dir = "dashboard"
    os.makedirs(js_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist. Please run prepare_data.py first.")
        return
        
    df = pd.read_csv(csv_path)
    
    # Select only columns needed for the dashboard to keep the file size reasonable
    cols = [
        'Order Date', 'Category', 'Sub-Category', 'Region', 
        'Customer Segment', 'Sales Revenue', 'Profit', 'Quantity Sold', 'Product Name'
    ]
    df_dashboard = df[cols]
    
    # Convert to list of dicts
    records = df_dashboard.to_dict(orient='records')
    
    # Output to dashboard/data.js
    output_path = os.path.join(js_dir, "data.js")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated sales data for the interactive HTML dashboard\n")
        f.write("const salesData = ")
        json.dump(records, f, ensure_ascii=False)
        f.write(";\n")
        
    print(f"Successfully exported data to {output_path} (Total records: {len(records)})")

if __name__ == "__main__":
    main()
