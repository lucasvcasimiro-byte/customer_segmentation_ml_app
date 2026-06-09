import pandas as pd
import ast
from collections import Counter

print("Loading customer_basket.csv...")
df = pd.read_csv('data/customer_basket.csv')

def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except:
        return []

print("Counting items...")
counter = Counter()
for val in df['list_of_goods']:
    goods = safe_eval(val)
    counter.update(goods)

print("Top 10 items:")
for item, count in counter.most_common(10):
    print(f"  {item}: {count}")
