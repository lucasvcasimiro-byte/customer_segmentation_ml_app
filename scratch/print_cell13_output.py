import json

with open('notebooks/basket_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell13 = nb['cells'][13]
outputs = cell13.get('outputs', [])

for i, out in enumerate(outputs):
    if 'text' in out:
        print("".join(out['text']))
    elif 'data' in out:
        if 'text/plain' in out['data']:
            print("".join(out['data']['text/plain']))
        elif 'text/html' in out['data']:
            # Maybe clean or print a bit of it
            html = "".join(out['data']['text/html'])
            print(f"[HTML output length {len(html)}]")
