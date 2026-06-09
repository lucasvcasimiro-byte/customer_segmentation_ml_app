import pandas as pd
import numpy as np
import umap
from sklearn.preprocessing import RobustScaler
import json
import os

print("Starting UMAP calculation script...")

# 1. Load preprocessed clustered dataset
df = pd.read_csv('data/ci_clustered.csv')
print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")

# 2. Define the exact features used for clustering
FEATURE_COLS = [
    'age',
    'dependants',
    'education_level',
    'customer_tenure',
    'distinct_stores_visited',
    'typical_hour',
    'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products',
    'number_complaints',
    'total_spend',
    'share_electronics',
    'share_vegetables',
    'share_nonalcohol_drinks',
    'share_alcohol_drinks',
    'share_meat',
    'share_fish',
    'share_hygiene',
    'share_videogames',
    'share_petfood'
]

# 3. Standardize feature values using RobustScaler (as in the notebook)
X = df[FEATURE_COLS].copy()
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
print("Scaled features using RobustScaler.")

# 4. Compute UMAP coordinates using the notebook's hyperparameters (random_state=42, n_neighbors=15, min_dist=0.1)
print("Running UMAP dimensionality reduction (this might take a minute)...")
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
coords = reducer.fit_transform(X_scaled)
print("UMAP coordinates generated.")

# 5. Extract UMAP dimensions and cluster assignments
df_coords = pd.DataFrame({
    'umap_1': coords[:, 0],
    'umap_2': coords[:, 1],
    'cluster': df['final_cluster_nr']
})

# 6. Sample 100 points per cluster to keep the Plotly interactive scatter plot smooth and fast
sampled_groups = []
for cluster_nr in sorted(df_coords['cluster'].unique()):
    cluster_df = df_coords[df_coords['cluster'] == cluster_nr]
    sampled_cluster = cluster_df.sample(n=min(100, len(cluster_df)), random_state=42)
    sampled_groups.append({
        'cluster': int(cluster_nr),
        'x': [round(val, 4) for val in sampled_cluster['umap_1'].tolist()],
        'y': [round(val, 4) for val in sampled_cluster['umap_2'].tolist()]
    })
    print(f"Sampled {len(sampled_cluster)} points for cluster {cluster_nr}.")

# 7. Write results to JSON
output_path = 'data/umap_sampled.json'
with open(output_path, 'w') as f:
    json.dump(sampled_groups, f, indent=2)

print(f"UMAP coordinates saved to {output_path} successfully!")
