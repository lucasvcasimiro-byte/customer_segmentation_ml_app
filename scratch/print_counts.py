import json

with open('notebooks/segmentation_fixed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell54 = nb['cells'][54]
outputs = cell54.get('outputs', [])
for out in outputs:
    if 'text' in out:
        print("".join(out['text']))
    elif 'data' in out and 'text/plain' in out['data']:
        print("".join(out['data']['text/plain']))
