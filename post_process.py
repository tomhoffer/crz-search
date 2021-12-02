import pandas as pd

lines = pd.read_json('output.jl', lines=True)

# Drop duplicate items (just in case)
lines = lines.drop_duplicates(subset='url')

# Replace newlines with spaces
lines = lines.replace(r'\r+|\n+|\t+', ' ', regex=True)

# Remove trailing spaces
lines['customer'] = lines['customer'].str.strip()
lines['supplier'] = lines['supplier'].str.strip()
lines['customer_address'] = lines['customer_address'].str.strip()
lines['supplier_address'] = lines['supplier_address'].str.strip()

# Unify name capitalization
lines['customer'] = lines['customer'].str.upper()
lines['supplier'] = lines['supplier'].str.upper()

lines.to_csv('output.csv')
