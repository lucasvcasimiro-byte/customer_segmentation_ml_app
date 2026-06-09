import pandas as pd
import json

df = pd.read_csv('data/ci_clustered.csv')
total_cust = len(df)
avg_spend = df['total_spend'].mean()

print(f"Total customers: {total_cust}")
print(f"Avg spend: {avg_spend:.2f}")

# Let's search the segmentation notebook for the silhouette score of rb_ward7
with open('notebooks/segmentation_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    source = "".join(cell.get('source', []))
    if 'rb_ward7' in source or 'silhouette' in source:
        for out in cell.get('outputs', []):
            text = "".join(out.get('text', []))
            if text:
                print("--- Output block ---")
                print(text[:1000])
