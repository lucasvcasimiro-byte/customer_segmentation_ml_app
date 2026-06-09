import re

# Update server.py
print("Updating server.py...")
with open('server.py', 'r', encoding='utf-8') as f:
    server_content = f.read()

# Replace CLUSTERING_FILE and remove kmeans / scaling logic
target_data = """CLUSTERING_FILE = os.path.join(DATA_DIR, 'ci_clustering.csv')
BASKET_FILE = os.path.join(DATA_DIR, 'customer_basket.csv')
RULES_FILE = os.path.join(DATA_DIR, 'cluster_association_rules.json')

# 2. Carregar e indexar dados dos clientes
print("A carregar base de dados de clientes (ci_clustering.csv)...")
df_ci = pd.read_csv(CLUSTERING_FILE)
print(f"Carregados {len(df_ci)} clientes com sucesso!")

# Colunas de características (features)
FEATURE_COLS = [
    'age', 'is_female', 'dependants', 'education_level',
    'vegetarian', 'pescatarian', 'carnivore', 'omnivore',
    'has_loyalty_card', 'customer_tenure', 'distinct_stores_visited',
    'typical_hour', 'percentage_of_products_bought_promotion',
    'lifetime_total_distinct_products', 'number_complaints',
    'total_spend',
    'share_groceries', 'share_electronics', 'share_vegetables',
    'share_nonalcohol_drinks', 'share_alcohol_drinks', 'share_meat',
    'share_fish', 'share_hygiene', 'share_videogames', 'share_petfood',
    'latitude', 'longitude'
]

print("A normalizar características...")
scaler = StandardScaler()
X = scaler.fit_transform(df_ci[FEATURE_COLS])

print("A treinar modelo K-Means (K=6)...")
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
df_ci['cluster'] = kmeans.fit_predict(X)
print("Treino concluído com sucesso!")"""

replacement_data = """CLUSTERING_FILE = os.path.join(DATA_DIR, 'ci_clustered.csv')
BASKET_FILE = os.path.join(DATA_DIR, 'customer_basket.csv')
RULES_FILE = os.path.join(DATA_DIR, 'cluster_association_rules.json')

# 2. Carregar e indexar dados dos clientes
print("A carregar base de dados de clientes (ci_clustered.csv)...")
df_ci = pd.read_csv(CLUSTERING_FILE)
print(f"Carregados {len(df_ci)} clientes com sucesso!")"""

if target_data in server_content:
    server_content = server_content.replace(target_data, replacement_data)
else:
    # Try with single quotes or slight variations
    print("Warning: target_data not found in server.py. Trying regex or manual replacement.")

# Replace cluster_rules default creation (range(6) to range(7))
server_content = re.sub(
    r'cluster_rules = \{str\(i\): \[\] for i in range\(6\)\}',
    'cluster_rules = {str(i): [] for i in range(7)}',
    server_content
)

# Replace CLUSTER_SEGMENTS
# Find the start of CLUSTER_SEGMENTS and the end
segments_start = server_content.find("CLUSTER_SEGMENTS = {")
if segments_start != -1:
    # Let's find the closing brace of CLUSTER_SEGMENTS. It is followed by "# 6. Lógica de recomendação híbrida"
    segments_end = server_content.find("# 6. Lógica de recomendação híbrida")
    if segments_end != -1:
        # Extract and replace
        old_segments = server_content[segments_start:segments_end]
        new_segments = """CLUSTER_SEGMENTS = {
    0: {
        'segment': 'Vegans',
        'discount': '15%',
        'nextBestOffer': '15% off Organic Vegetables Subscription',
        'campaignItems': ['napkins', 'babies food', 'cooking oil'],
        'items': ['napkins', 'babies food', 'cooking oil'],
        'propensity': 0.88
    },
    1: {
        'segment': 'Loyal core spenders',
        'discount': '10%',
        'nextBestOffer': '10% off Grocery Essentials',
        'campaignItems': ['eggs', 'cereals', 'fresh bread'],
        'items': ['eggs', 'cereals', 'fresh bread'],
        'propensity': 0.32
    },
    2: {
        'segment': 'Big families (big spenders)',
        'discount': '15%',
        'nextBestOffer': '15% off Family Bulk Packs',
        'campaignItems': ['honey', 'milk', 'oatmeal', 'cereals'],
        'items': ['honey', 'milk', 'oatmeal', 'cereals'],
        'propensity': 0.85
    },
    3: {
        'segment': 'Bargain hunters',
        'discount': '25%',
        'nextBestOffer': '25% off Promotional Items',
        'campaignItems': ['laptop', 'energy drink', 'bluetooth headphones'],
        'items': ['laptop', 'energy drink', 'bluetooth headphones'],
        'propensity': 0.55
    },
    4: {
        'segment': 'Gamers',
        'discount': '10%',
        'nextBestOffer': '10% off Gaming Snack Bundles',
        'campaignItems': ['airpods', 'iphone 10', 'energy drink', 'bluetooth headphones'],
        'items': ['airpods', 'iphone 10', 'energy drink', 'bluetooth headphones'],
        'propensity': 0.77
    },
    5: {
        'segment': 'Karens',
        'discount': '10%',
        'nextBestOffer': '10% off Next Purchase & Priority Support',
        'campaignItems': ['salad', 'tomatoes', 'carrots', 'frozen vegetables'],
        'items': ['salad', 'tomatoes', 'carrots', 'frozen vegetables'],
        'propensity': 0.65
    },
    6: {
        'segment': 'Tech enthusiasts',
        'discount': '12%',
        'nextBestOffer': '12% off Late-Hour Electronics Deals',
        'campaignItems': ['energy drink', 'airpods', 'gadget for tiktok streaming', 'bluetooth headphones'],
        'items': ['energy drink', 'airpods', 'gadget for tiktok streaming', 'bluetooth headphones'],
        'propensity': 0.79
    }
}

"""
        server_content = server_content.replace(old_segments, new_segments)

# Update range(6) to range(7) in recommend_items
server_content = re.sub(
    r'for c_id in range\(6\):',
    'for c_id in range(7):',
    server_content
)

# Update get_recommendations logic
old_rec_block = """    row = customer_lookup[customer_id]
    cluster_idx = int(row['cluster'])
    profile = CLUSTER_SEGMENTS[cluster_idx]
    
    # 3. Lógica adaptativa em tempo real com base no cesto de compras
    segment_name = profile['segment']
    next_best_offer = profile['nextBestOffer']
    
    basket_lower = [item.lower() for item in basket_found]
    has_meat = any(x in basket_lower for x in ['ground beef', 'chicken', 'salmon', 'bacon', 'beef', 'fish', 'shrimp', 'pork'])
    has_electronics = any(x in basket_lower for x in ['ring light', 'airpods', 'headphones', 'earbuds', 'samsung', 'galaxy', 'iphone'])
    
    # Adaptação dinâmica para o Cluster 1 (Vegetable Heavy)
    campaign_items = profile['campaignItems'][:]
    if cluster_idx == 1:
        if has_meat:
            segment_name = 'Vegetable Heavy / Flexitarian'
            next_best_offer = '15% off Fresh Produce & Protein Bundle'
            campaign_items = ['asparagus', 'salmon', 'chicken']   # vegetais + proteína
        elif has_electronics:
            segment_name = 'Healthy Tech Shopper'
            next_best_offer = '15% off Smart Kitchen & Fresh Produce'
            campaign_items = ['asparagus', 'spinach', 'tomatoes']
            
    # 4. Calcular itens de cross-sell via regras de associação
    cross_sell_items = recommend_items(cluster_idx, basket_found)
    
    # 5. Construir resposta combinada
    response = {
        'customerId': customer_id,
        'invoiceId': invoice_id,
        'customerName': str(row['customer_name']),
        'customerGender': str(row['customer_gender']),
        'age': int(row['age']),
        'segment': segment_name,
        'discount': profile['discount'],
        'nextBestOffer': next_best_offer,
        'basket': basket_found,
        'campaignItems': campaign_items,         # itens sobre os quais o desconto se aplica
        'items': cross_sell_items,               # sugestões adicionais de cross-selling
        'propensity': float(row['percentage_of_products_bought_promotion'] if cluster_idx == 0 else profile['propensity']),
        'totalSpend': float(row['total_spend']),
        'algorithm': 'K-Means (K=6) + Apriori (Real-Time)'
    }"""

new_rec_block = """    row = customer_lookup[customer_id]
    cluster_idx = int(row['final_cluster_nr'])
    profile = CLUSTER_SEGMENTS[cluster_idx]
    
    # 3. Lógica adaptativa em tempo real com base no cesto de compras
    segment_name = profile['segment']
    next_best_offer = profile['nextBestOffer']
    
    basket_lower = [item.lower() for item in basket_found]
    has_meat = any(x in basket_lower for x in ['ground beef', 'chicken', 'salmon', 'bacon', 'beef', 'fish', 'shrimp', 'pork'])
    has_electronics = any(x in basket_lower for x in ['ring light', 'airpods', 'headphones', 'earbuds', 'samsung', 'galaxy', 'iphone'])
    
    # Adaptação dinâmica para o Cluster 0 (Vegans)
    campaign_items = profile['campaignItems'][:]
    if cluster_idx == 0:
        if has_meat:
            segment_name = 'Vegan / Flexitarian'
            next_best_offer = '15% off Fresh Produce & Protein Bundle'
            campaign_items = ['napkins', 'salmon', 'chicken']
        elif has_electronics:
            segment_name = 'Vegan Tech Shopper'
            next_best_offer = '15% off Veggies & Kitchen Appliances'
            campaign_items = ['napkins', 'cooking oil', 'tomatoes']
            
    # 4. Calcular itens de cross-sell via regras de associação
    cross_sell_items = recommend_items(cluster_idx, basket_found)
    
    # 5. Construir resposta combinada
    response = {
        'customerId': customer_id,
        'invoiceId': invoice_id,
        'customerName': str(row['customer_name']),
        'customerGender': str(row['customer_gender']),
        'age': int(row['age']),
        'segment': segment_name,
        'discount': profile['discount'],
        'nextBestOffer': next_best_offer,
        'basket': basket_found,
        'campaignItems': campaign_items,         # itens sobre os quais o desconto se aplica
        'items': cross_sell_items,               # sugestões adicionais de cross-selling
        'propensity': float(row['percentage_of_products_bought_promotion'] if cluster_idx == 3 else profile['propensity']),
        'totalSpend': float(row['total_spend']),
        'algorithm': 'RobustScaler Ward (K=7) + Apriori (Real-Time)'
    }"""

if old_rec_block in server_content:
    server_content = server_content.replace(old_rec_block, new_rec_block)
else:
    print("Warning: old_rec_block not found in server.py.")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server_content)
print("server.py updated.")

# Update Clustering.jsx
print("Updating Clustering.jsx...")
with open('dashboard/src/sections/Clustering.jsx', 'r', encoding='utf-8') as f:
    clustering_content = f.read()

clustering_content = re.sub(
    r"const \[selectedScaler, setSelectedScaler\] = useState\('StandardScaler'\)",
    "const [selectedScaler, setSelectedScaler] = useState('RobustScaler')",
    clustering_content
)
clustering_content = re.sub(
    r"const \[selectedK, setSelectedK\]\s*=\s*useState\(6\)",
    "const [selectedK, setSelectedK]           = useState(7)",
    clustering_content
)

with open('dashboard/src/sections/Clustering.jsx', 'w', encoding='utf-8') as f:
    f.write(clustering_content)
print("Clustering.jsx updated.")
