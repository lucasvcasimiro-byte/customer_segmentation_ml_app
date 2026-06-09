import json

with open('notebooks/basket_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('scratch/basket_notebook_content.txt', 'w', encoding='utf-8') as out:
    for idx, cell in enumerate(nb.get('cells', [])):
        cell_type = cell.get('cell_type')
        source = ''.join(cell.get('source', []))
        out.write(f"=========================================\n")
        out.write(f"CELL {idx} - TYPE: {cell_type}\n")
        out.write(f"=========================================\n")
        out.write(source)
        out.write("\n\n")

print("Done!")
