import json

with open('scratch/flat_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

# Group rules by cluster
rules_by_cluster = {}
for r in rules:
    c = r['cluster']
    if c not in rules_by_cluster:
        rules_by_cluster[c] = []
    rules_by_cluster[c].append(r)

for c, cluster_rules in rules_by_cluster.items():
    print(f"=== Cluster: {c} (Total rules: {len(cluster_rules)}) ===")
    for r in cluster_rules[:3]:
        print(f"  {r['antecedents']} -> {r['consequents']} (Support: {r['support']:.4f}, Conf: {r['confidence']:.4f}, Lift: {r['lift']:.4f})")
