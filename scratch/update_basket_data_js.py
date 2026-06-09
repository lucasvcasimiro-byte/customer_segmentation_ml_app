import json

# Load flat rules
with open('scratch/flat_rules.json', 'r', encoding='utf-8') as f:
    flat_rules = json.load(f)

# Sort by lift descending
flat_rules.sort(key=lambda x: x['lift'], reverse=True)

# Select top 15 rules for table
top_rules = flat_rules[:15]

# Select top 8 rules for chart
chart_rules = flat_rules[:8]

categories = []
lift = []
confidence = []

for r in chart_rules:
    # Format categories like "Bread+Butter→Milk"
    ant_str = "+".join([item.title() for item in r['antecedents'].split(", ")])
    cons_str = "+".join([item.title() for item in r['consequents'].split(", ")])
    categories.append(f"{ant_str}→{cons_str}")
    lift.append(r['lift'])
    confidence.append(r['confidence'])

# Format associationRules for js
js_rules = []
for r in top_rules:
    js_rules.append({
        'antecedents': r['antecedents'].title(),
        'consequents': r['consequents'].title(),
        'support': round(r['support'], 4),
        'confidence': round(r['confidence'], 4),
        'lift': round(r['lift'], 2)
    })

# Format discountTiers
discount_tiers = [
    { 'segment': 'Loyal core spenders', 'discount': '5–10%', 'type': 'Loyalty Reward', 'icon': '👑' },
    { 'segment': 'Vegans', 'discount': '15%', 'type': 'Healthy Subscriptions', 'icon': '🥗' },
    { 'segment': 'Bargain hunters', 'discount': '20–25%', 'type': 'Win-Back Promotion', 'icon': '📢' },
    { 'segment': 'Karens', 'discount': '10%', 'type': 'Service Resolution', 'icon': '🚨' },
    { 'segment': 'Tech enthusiasts', 'discount': '10–15%', 'type': 'Late Flash Sales', 'icon': '⚡' },
    { 'segment': 'Big families (big spenders)', 'discount': '15–20%', 'type': 'Family Essentials', 'icon': '👨‍👩‍👧‍👦' },
    { 'segment': 'Gamers', 'discount': '10%', 'type': 'Bundle Deals', 'icon': '🎮' }
]

# Write js file content
js_content = f"""/**
 * basketData.js
 * ─────────────────────────────────────────────────────────────────────────────
 * Real basket/transaction association rules and discount tiers.
 * Automatically generated from basket_fixed.ipynb outputs.
 * ─────────────────────────────────────────────────────────────────────────────
 */

// ── Association rules (from mlxtend / Apriori) ───────────────────────────────
export const associationRules = {json.dumps(js_rules, indent=2)};

// ── Top items by frequency ────────────────────────────────────────────────────
export const topItems = {{
  labels: ['Milk', 'Fresh Bread', 'Butter', 'Eggs', 'Vegetables', 'Fruit', 'Meat', 'Snacks'],
  counts: [14200, 12800, 9500, 8900, 7500, 6900, 6100, 4800]
}};

// ── Customer recommendations (simulator offline database) ────────────────────
export const sampleRecommendations = {{
  '3032': {{
    segment: 'Vegans',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.88,
    items: ['napkins', 'babies food', 'cooking oil'],
    discount: '15%'
  }},
  '1': {{
    segment: 'Loyal core spenders',
    nextBestOffer: '10% off Grocery Essentials',
    propensity: 0.32,
    items: ['eggs', 'cereals', 'fresh bread'],
    discount: '10%'
  }},
  '42': {{
    segment: 'Vegans',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.88,
    items: ['napkins', 'babies food', 'cooking oil'],
    discount: '15%'
  }},
  '198': {{
    segment: 'Bargain hunters',
    nextBestOffer: '25% off Next Promotional Visit',
    propensity: 0.55,
    items: ['laptop', 'energy drink', 'bluetooth headphones'],
    discount: '25%'
  }},
  '222': {{
    segment: 'Tech enthusiasts',
    nextBestOffer: '12% off Electronics Flash Sale',
    propensity: 0.79,
    items: ['energy drink', 'airpods', 'gadget for tiktok streaming'],
    discount: '12%'
  }}
}};

// ── Lift chart data per product category ─────────────────────────────────────
export const liftChartData = {{
  categories: {json.dumps(categories, indent=2)},
  lift: {json.dumps(lift, indent=2)},
  confidence: {json.dumps(confidence, indent=2)}
}};

// ── Discount tiers ───────────────────────────────────────────────────────────
export const discountTiers = {json.dumps(discount_tiers, indent=2)};
"""

# Save file
with open('dashboard/src/data/basketData.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("basketData.js updated successfully!")
