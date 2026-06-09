import json

with open('notebooks/basket_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb.get('cells', [])):
    if idx >= 13:
        source = ''.join(cell.get('source', []))
        cell_type = cell.get('cell_type')
        print(f'=== Cell {idx} ({cell_type}) ===')
        print(source[:1000])
        print('...\n')
