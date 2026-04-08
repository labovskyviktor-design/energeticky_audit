
import pandas as pd
import os

filepath = "docs/excel/03_Pomôcka - bilancia VYK a TV(1).xlsx"
xl = pd.ExcelFile(filepath)

print(f"Sheets in {filepath}: {xl.sheet_names}")

output_dir = "docs/excel_dump"
os.makedirs(output_dir, exist_ok=True)

for sheet in xl.sheet_names:
    try:
        df = pd.read_excel(filepath, sheet_name=sheet)
        csv_path = os.path.join(output_dir, f"{sheet}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {sheet} to {csv_path}")
    except Exception as e:
        print(f"Error reading sheet {sheet}: {e}")
