with open('scratch/basket_notebook_content.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_cell = None
cell_lines = []

for line in lines:
    if line.startswith("========================================="):
        if cell_lines and current_cell:
            # check if we want to print this cell
            cell_idx = int(current_cell.split()[1])
            if 5 <= cell_idx <= 13:
                print(f"=== {current_cell} ===")
                print("".join(cell_lines))
                print("\n")
            cell_lines = []
        current_cell = None
    elif line.startswith("CELL "):
        current_cell = line.strip()
    elif current_cell:
        cell_lines.append(line)
