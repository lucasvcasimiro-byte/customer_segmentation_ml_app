import pandas as pd

df = pd.read_csv('data/ci_clustered.csv')
total_cust = len(df)

cluster_order = [
    'Loyal core spenders',
    'Vegans',
    'Bargain hunters',
    'Karens',
    'Tech enthusiasts',
    'Big families (big spenders)',
    'Gamers'
]

# Mapping cluster to emoji and tags
cluster_meta = {
    'Loyal core spenders': {
        'emoji': '👑',
        'color': '#f43f5e',
        'colorLight': 'rgba(244,63,94,0.15)',
        'colorBorder': 'rgba(244,63,94,0.35)',
        'badgeClass': 'badge-rose',
        'tags': ['High LTV', 'Loyal', 'High Spend'],
        'desc': 'Highest average lifetime spend, high transaction frequency, and high loyalty card penetration. They are the core revenue drivers.'
    },
    'Vegans': {
        'emoji': '🥗',
        'color': '#2dd4bf',
        'colorLight': 'rgba(45,212,191,0.15)',
        'colorBorder': 'rgba(45,212,191,0.35)',
        'badgeClass': 'badge-teal',
        'tags': ['Healthy Diet', 'Vegetables Heavy', 'Low Complaints'],
        'desc': 'Older customer segment with high vegetables and fresh food expenditure shares. Receptive to healthy subscription programs.'
    },
    'Bargain hunters': {
        'emoji': '📢',
        'color': '#f59e0b',
        'colorLight': 'rgba(245,158,11,0.15)',
        'colorBorder': 'rgba(245,158,11,0.35)',
        'badgeClass': 'badge-amber',
        'tags': ['Promo-Driven', 'Price-Conscious', 'Mid Spend'],
        'desc': 'Strongly driven by discounts and promotions. High share of purchases on promotion, moderate overall spend.'
    },
    'Karens': {
        'emoji': '🚨',
        'color': '#ec4899',
        'colorLight': 'rgba(236,72,153,0.15)',
        'colorBorder': 'rgba(236,72,153,0.35)',
        'badgeClass': 'badge-rose',
        'tags': ['High Complaints', 'Support Intensive', 'Churn Risk'],
        'desc': 'Highest average rate of customer service complaints. Requires proactive customer service outreach to minimize churn risk.'
    },
    'Tech enthusiasts': {
        'emoji': '⚡',
        'color': '#06b6d4',
        'colorLight': 'rgba(6,182,212,0.15)',
        'colorBorder': 'rgba(6,182,212,0.35)',
        'badgeClass': 'badge-cyan',
        'tags': ['Electronics Heavy', 'Tech-Driven', 'Singles/Couples'],
        'desc': 'High share of spend in electronics and gadgets. Shop mostly in the evening/late hours with low dependants counts.'
    },
    'Big families (big spenders)': {
        'emoji': '👨‍👩‍👧‍👦',
        'color': '#3b82f6',
        'colorLight': 'rgba(59,130,246,0.15)',
        'colorBorder': 'rgba(59,130,246,0.35)',
        'badgeClass': 'badge-blue',
        'tags': ['Large Family', 'Wide Variety', 'High Spend'],
        'desc': 'High dependants count (average 7+), buying a massive variety of distinct products across grocery and household items.'
    },
    'Gamers': {
        'emoji': '🎮',
        'color': '#a78bfa',
        'colorLight': 'rgba(167,139,250,0.15)',
        'colorBorder': 'rgba(167,139,250,0.35)',
        'badgeClass': 'badge-purple',
        'tags': ['Videogames Heavy', 'Younger Age', 'Leisure'],
        'desc': 'Heavy spending on videogames and related digital entertainment. Receptive to gaming accessories and snack bundles.'
    }
}

# Calculate normalizer ranges for radar chart
# Spending: 0-100 (normalized total_spend)
# Frequency: 0-100 (normalized distinct_stores_visited or tenure/frequency)
# Recency: 0-100 (normalized typical_hour / age etc.) Let's just use nice visual radar metrics aligned with the means:
# Spending = Avg Spend / 50000 * 100
# Variety = Avg distinct products / max distinct products * 100
# Complaints = Avg complaints / 3 * 100
# Promotion = Avg promo pct * 100
# Loyalty = Avg has loyalty card * 100

print("Calculating metrics per cluster:")
for idx, name in enumerate(cluster_order):
    group = df[df['final_cluster_label'] == name]
    count = len(group)
    pct = (count / total_cust) * 100
    avg_spend = group['total_spend'].mean()
    
    # Calculate some radar features
    avg_promo = group['percentage_of_products_bought_promotion'].mean() * 100
    avg_complaints = group['number_complaints'].mean()
    avg_loyalty = group['has_loyalty_card'].mean() * 100
    avg_variety = group['lifetime_total_distinct_products'].mean()
    avg_dependants = group['dependants'].mean()
    
    # Normalizations for radar
    spending_score = min(100, int(avg_spend / 38000 * 100))
    promo_score = min(100, int(avg_promo))
    complaints_score = min(100, int(avg_complaints / 2.5 * 100))
    loyalty_score = min(100, int(avg_loyalty))
    variety_score = min(100, int(avg_variety / 85 * 100))
    
    print(f"Cluster: {name}")
    print(f"  ID: {idx}")
    print(f"  Count: {count}")
    print(f"  Percentage: {pct:.2f}%")
    print(f"  Avg Spend: €{avg_spend:.2f}")
    print(f"  Radar: Spending={spending_score}, Promo={promo_score}, Complaints={complaints_score}, Loyalty={loyalty_score}, Variety={variety_score}")
    print("-" * 30)
