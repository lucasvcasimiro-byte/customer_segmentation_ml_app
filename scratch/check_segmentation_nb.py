import json

with open('notebooks/segmentation_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb.get('cells', [])):
    source = ''.join(cell.get('source', []))
    if any(w in source.lower() for w in ['cluster', 'label', 'silhouette', 'group', 'mapping', 'name']) and cell.get('cell_type') == 'code':
        # print some info about code cells
        print(f"=== Cell {idx} ===")
        print(source[:500])
        print("...")
