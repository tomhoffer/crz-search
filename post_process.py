import pandas as pd

lines = pd.read_json('output.jl', lines=True)

lines = lines.drop_duplicates(subset='url')

lines.to_csv('output.csv')