import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(num_customers=1000, num_rows=5000):
    np.random.seed(42)
    
    # Generate Customer IDs
    customer_ids = [f"C-{1000 + i}" for i in range(num_customers)]
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_rows):
        cid = np.random.choice(customer_ids)
        
        # Randomize behavior: some customers are recent, some are old
        days_to_add = np.random.randint(0, 800) 
        transaction_date = start_date + timedelta(days=days_to_add)
        
        # Randomize spend: normal distribution around $50
        amount = np.abs(np.random.normal(50, 30)) + 5.0
        
        data.append([cid, transaction_date.strftime('%Y-%m-%d'), round(amount, 2)])
    
    df = pd.DataFrame(data, columns=['CustomerID', 'TransactionDate', 'TransactionAmount'])
    
    # Save to CSV
    df.to_csv('mock_sales_data.csv', index=False)
    print(f"✅ Success! Created 'mock_sales_data.csv' with {num_rows} transactions.")

if __name__ == "__main__":
    generate_mock_data()