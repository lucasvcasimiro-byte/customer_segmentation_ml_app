import pandas as pd
df = pd.read_csv('data/ci_clustered.csv')
print(df.columns)
print(df[['customer_id', 'final_cluster_nr', 'final_cluster_label']].head())
