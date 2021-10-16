import pandas as pd

lines = pd.read_json('output.jl', lines=True)

# Drop duplicate items (just in case)
lines = lines.drop_duplicates(subset='url')

# Remove trailing spaces
lines['customer'] = lines['customer'].str.strip()
lines['supplier'] = lines['supplier'].str.strip()
lines['customer_address'] = lines['customer_address'].str.strip()
lines['supplier_address'] = lines['supplier_address'].str.strip()

lines.to_csv('output.csv')