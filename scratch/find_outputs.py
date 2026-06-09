import json

with open('notebooks/basket_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') != 'code':
        continue
    outputs = cell.get('outputs', [])
    if not outputs:
        continue
    
    # Check if there is text output or display data (like tables)
    text_data = ""
    for out in outputs:
        if 'text' in out:
            text_data += ''.join(out['text'])
        elif 'data' in out and 'text/plain' in out['data']:
            text_data += ''.join(out['data']['text/plain'])
        elif 'data' in out and 'text/html' in out['data']:
            text_data += ''.join(out['data']['text/html'])
            
    if any(w in text_data.lower() for w in ['antecedents', 'consequents', 'lift', 'support', 'confidence']):
        print(f"Cell {idx} has rules/metrics in output. Length of output text: {len(text_data)}")
        print("First 500 chars of output:")
        print(text_data[:500])
        print("-" * 50)
