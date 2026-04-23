import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data():
    np.random.seed(42)
    random.seed(42)

    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Electronics', 'Furniture', 'Clothing', 'Food & Beverages', 'Sports']
    products = {
        'Electronics': ['Laptop', 'Mobile', 'Tablet', 'Headphones', 'Smart Watch'],
        'Furniture': ['Office Chair', 'Desk', 'Bookshelf', 'Sofa', 'Wardrobe'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'],
        'Food & Beverages': ['Coffee', 'Tea', 'Snacks', 'Beverages', 'Dairy'],
        'Sports': ['Cricket Bat', 'Football', 'Gym Equipment', 'Yoga Mat', 'Cycle']
    }
    sales_reps = ['Amit Sharma', 'Priya Singh', 'Rahul Verma', 'Neha Gupta',
                  'Suresh Patel', 'Anita Joshi', 'Vikram Rao', 'Kavita Nair']
    segments = ['Enterprise', 'SMB', 'Retail', 'Government']

    rows = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    for _ in range(5000):
        category = random.choice(categories)
        product = random.choice(products[category])
        region = random.choice(regions)
        segment = random.choice(segments)
        sales_rep = random.choice(sales_reps)

        order_date = start_date + timedelta(days=random.randint(0, date_range))
        quantity = random.randint(1, 50)

        base_price = {'Electronics': 25000, 'Furniture': 8000, 'Clothing': 1500,
                      'Food & Beverages': 500, 'Sports': 3000}[category]
        unit_price = base_price * np.random.uniform(0.7, 1.5)
        revenue = round(quantity * unit_price, 2)
        cost = round(revenue * np.random.uniform(0.4, 0.7), 2)
        profit = round(revenue - cost, 2)
        discount = round(np.random.uniform(0, 0.3), 2)

        rows.append({
            'order_id': f'ORD-{random.randint(10000, 99999)}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'region': region,
            'segment': segment,
            'category': category,
            'product': product,
            'sales_rep': sales_rep,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'discount': discount,
            'profit_margin': round((profit / revenue) * 100, 2) if revenue > 0 else 0
        })

    df = pd.DataFrame(rows)
    df.to_csv('sales_data.csv', index=False)
    return df

if __name__ == '__main__':
    df = generate_sales_data()
    print(f"Generated {len(df)} sales records")
    print(df.head())
