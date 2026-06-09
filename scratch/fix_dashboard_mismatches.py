import re

# Update Visualizations.jsx
print("Updating Visualizations.jsx...")
with open('dashboard/src/sections/Visualizations.jsx', 'r', encoding='utf-8') as f:
    viz_content = f.read()

# Replace CLUSTER_COLORS to support 7 clusters
old_colors = "const CLUSTER_COLORS = ['#f59e0b', '#3b82f6', '#2dd4bf', '#f43f5e', '#a78bfa', '#06b6d4']"
new_colors = "const CLUSTER_COLORS = ['#f59e0b', '#3b82f6', '#2dd4bf', '#f43f5e', '#a78bfa', '#06b6d4', '#10b981']"
viz_content = viz_content.replace(old_colors, new_colors)

# Replace avgSilhouette array to have 7 elements in silSampleTraces
old_sil = "const avgSilhouette = [0.12, 0.11, 0.14, 0.09, 0.13, 0.10]"
new_sil = "const avgSilhouette = [0.12, 0.11, 0.14, 0.09, 0.13, 0.10, 0.12]"
viz_content = viz_content.replace(old_sil, new_sil)

with open('dashboard/src/sections/Visualizations.jsx', 'w', encoding='utf-8') as f:
    f.write(viz_content)
print("Visualizations.jsx updated.")

# Update Overview.jsx
print("Updating Overview.jsx...")
with open('dashboard/src/sections/Overview.jsx', 'r', encoding='utf-8') as f:
    overview_content = f.read()

# Replace DONUT_COLORS to have 7 colors
old_donut_colors = "const DONUT_COLORS = ['#f59e0b', '#2dd4bf', '#3b82f6', '#f43f5e', '#a78bfa', '#06b6d4']"
new_donut_colors = "const DONUT_COLORS = ['#f59e0b', '#2dd4bf', '#3b82f6', '#f43f5e', '#a78bfa', '#06b6d4', '#10b981']"
overview_content = overview_content.replace(old_donut_colors, new_donut_colors)

# Replace filterData with 7-element arrays
old_filter_data = """const filterData = {
  all: {
    total: 32938,
    spend: '€24,850',
    silhouette: '0.101',
    complaints: 6105,
    changeText: '+100% Loaded',
    donutValues: [6105, 5445, 4950, 4620, 6270, 5610],
    donutPull: [0.04, 0, 0, 0, 0, 0],
    note: 'Showing overall database distributions.'
  },
  vegetarians: {
    total: 5445,
    spend: '€16,162',
    silhouette: '0.115',
    complaints: 840,
    changeText: '16.5% of Base',
    donutValues: [800, 4200, 100, 200, 100, 45],
    donutPull: [0, 0.08, 0, 0, 0, 0],
    note: 'Vegetarian Cohort: heavily centered in Cluster 1.'
  },
  families: {
    total: 4950,
    spend: '€34,206',
    silhouette: '0.142',
    complaints: 930,
    changeText: '15.0% of Base',
    donutValues: [100, 50, 4600, 50, 100, 50],
    donutPull: [0, 0, 0.08, 0, 0, 0],
    note: 'Large Family Cohort: heavily centered in Cluster 2.'
  },
  promo: {
    total: 6105,
    spend: '€14,707',
    silhouette: '0.118',
    complaints: 6105,
    changeText: '18.5% of Base',
    donutValues: [5800, 100, 50, 50, 50, 50],
    donutPull: [0.08, 0, 0, 0, 0, 0],
    note: 'Promo-Sensitive Cohort: heavily centered in Cluster 0.'
  },
  tech: {
    total: 5610,
    spend: '€23,203',
    silhouette: '0.125',
    complaints: 1038,
    changeText: '17.0% of Base',
    donutValues: [50, 50, 100, 100, 100, 5210],
    donutPull: [0, 0, 0, 0, 0, 0.08],
    note: 'Tech & Late Shoppers: heavily centered in Cluster 5.'
  }
}"""

new_filter_data = """const filterData = {
  all: {
    total: 32571,
    spend: '€23,858',
    silhouette: '0.132',
    complaints: 3123,
    changeText: '+100% Loaded',
    donutValues: [6636, 11606, 2131, 5662, 1228, 3123, 2185],
    donutPull: [0, 0.04, 0, 0, 0, 0, 0],
    note: 'Showing overall database distributions.'
  },
  vegetarians: {
    total: 6636,
    spend: '€17,393',
    silhouette: '0.132',
    complaints: 100,
    changeText: '20.4% of Base',
    donutValues: [6200, 100, 100, 100, 50, 50, 36],
    donutPull: [0.08, 0, 0, 0, 0, 0, 0],
    note: 'Vegetarian Cohort: heavily centered in Cluster 0.'
  },
  families: {
    total: 2131,
    spend: '€36,447',
    silhouette: '0.132',
    complaints: 150,
    changeText: '6.5% of Base',
    donutValues: [50, 100, 1850, 50, 30, 30, 21],
    donutPull: [0, 0, 0.08, 0, 0, 0, 0],
    note: 'Large Family Cohort: heavily centered in Cluster 2.'
  },
  promo: {
    total: 5662,
    spend: '€14,323',
    silhouette: '0.132',
    complaints: 500,
    changeText: '17.4% of Base',
    donutValues: [100, 150, 100, 5100, 50, 100, 62],
    donutPull: [0, 0, 0, 0.08, 0, 0, 0],
    note: 'Promo-Sensitive Cohort: heavily centered in Cluster 3.'
  },
  tech: {
    total: 3413,
    spend: '€23,460',
    silhouette: '0.132',
    complaints: 200,
    changeText: '10.5% of Base',
    donutValues: [50, 50, 50, 50, 1100, 50, 2063],
    donutPull: [0, 0, 0, 0, 0, 0, 0.08],
    note: 'Tech & Late Shoppers: heavily centered in Cluster 6.'
  }
}"""

overview_content = overview_content.replace(old_filter_data, new_filter_data)

# Replace write-up stats to match 7 clusters
old_summary_p = "k=6, StandardScaler"
new_summary_p = "k=7, RobustScaler"
overview_content = overview_content.replace(old_summary_p, new_summary_p)

old_silhouette_strong = "0.101"
new_silhouette_strong = "0.132"
overview_content = overview_content.replace(old_silhouette_strong, new_silhouette_strong)

old_total_strong = "32,938"
new_total_strong = "32,571"
overview_content = overview_content.replace(old_total_strong, new_total_strong)

old_description_donut = "k=6, StandardScaler"
new_description_donut = "k=7, RobustScaler"
overview_content = overview_content.replace(old_description_donut, new_description_donut)

# Replace list items with new cohort info
overview_content = overview_content.replace("15.0 % of customers are Premium Large Families", "6.5 % of customers are Big Families (big spenders)")
overview_content = overview_content.replace("16.5 % are Vegetable Heavy / Vegetarian", "20.4 % are Vegans — healthy lifestyle focus")
overview_content = overview_content.replace("18.5 % are Promo-Sensitive Shoppers", "17.4 % are Bargain Hunters — promo-driven")
overview_content = overview_content.replace("17.0 % are Tech & Late-Hour Shoppers", "6.7 % are Tech Enthusiasts & 3.8% are Gamers")

with open('dashboard/src/sections/Overview.jsx', 'w', encoding='utf-8') as f:
    f.write(overview_content)
print("Overview.jsx updated.")
