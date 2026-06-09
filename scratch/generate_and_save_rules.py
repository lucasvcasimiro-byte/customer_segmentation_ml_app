import pandas as pd
import json
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath("."))

from functions.basket import generate_association_rules

# Load data
print("Loading customer_basket.csv...")
customer_basket = pd.read_csv('data/customer_basket.csv')
print("Loading ci_clustered.csv...")
customer = pd.read_csv('data/ci_clustered.csv')

# Prep cluster dataframes
cluster_dataframes = {
    cluster: group
    for cluster, group in customer.groupby("final_cluster_label")
}

# Parameters from basket_fixed.ipynb Cell 9
params_by_cluster = {
    "Loyal core spenders": {
        "min_support": 0.02,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Vegans": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Bargain hunters": {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    },
    "Karens": {
        "min_support": 0.008,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Tech enthusiasts": {
        "min_support": 0.006,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Big families (big spenders)": {
        "min_support": 0.006,
        "min_threshold": 1,
        "min_confidence": 0.08
    },
    "Gamers": {
        "min_support": 0.004,
        "min_threshold": 1,
        "min_confidence": 0.06
    }
}

cluster_mapping_by_name = {
    'Vegans': 0,
    'Loyal core spenders': 1,
    'Big families (big spenders)': 2,
    'Bargain hunters': 3,
    'Gamers': 4,
    'Karens': 5,
    'Tech enthusiasts': 6
}

serializable_rules = {}
all_flat_rules = []

for cluster_name, cluster_df in cluster_dataframes.items():
    print(f"\n--- Processing cluster: {cluster_name} (size: {len(cluster_df)}) ---")
    params = params_by_cluster.get(cluster_name, {
        "min_support": 0.01,
        "min_threshold": 1,
        "min_confidence": 0.10
    })
    
    print(f"Params: min_support={params['min_support']}, min_confidence={params['min_confidence']}")
    
    rules_df = generate_association_rules(
        customers=cluster_df,
        basket=customer_basket,
        min_support=params["min_support"],
        metric="lift",
        min_threshold=params["min_threshold"],
        min_confidence=params["min_confidence"]
    )
    
    cluster_id = cluster_mapping_by_name[cluster_name]
    formatted_rules = []
    
    if not rules_df.empty:
        print(f"Found {len(rules_df)} rules!")
        # Sort by lift descending
        rules_df = rules_df.sort_values(by='lift', ascending=False)
        for _, row in rules_df.iterrows():
            rule_dict = {
                'antecedents': list(row['antecedents']),
                'consequents': list(row['consequents']),
                'support': float(row['support']),
                'confidence': float(row['confidence']),
                'lift': float(row['lift'])
            }
            formatted_rules.append(rule_dict)
            
            # For the flat list (used in front-end)
            flat_rule_dict = {
                'cluster': cluster_name,
                'antecedents': ", ".join(list(row['antecedents'])),
                'consequents': ", ".join(list(row['consequents'])),
                'support': float(row['support']),
                'confidence': float(row['confidence']),
                'lift': float(row['lift'])
            }
            all_flat_rules.append(flat_rule_dict)
    else:
        print("No rules found.")
            
    # Save under both name and id
    serializable_rules[str(cluster_id)] = formatted_rules
    serializable_rules[cluster_name] = formatted_rules

# Save cluster rules json for backend server
output_json_path = 'data/cluster_association_rules.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(serializable_rules, f, ensure_ascii=False, indent=2)
print(f"\nSaved cluster rules to {output_json_path}")

# Sort flat rules for front-end by lift descending
all_flat_rules.sort(key=lambda x: x['lift'], reverse=True)
print(f"Total flat rules generated: {len(all_flat_rules)}")

# Save flat rules
with open('scratch/flat_rules.json', 'w', encoding='utf-8') as f:
    json.dump(all_flat_rules, f, indent=2)

print("Done!")
