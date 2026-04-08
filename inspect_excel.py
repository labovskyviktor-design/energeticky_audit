
import pandas as pd
import sys

files = [
    "docs/excel/01_Pomôcka - klimatické údaje.xlsx",
    "docs/excel/02_Pomôcka - obehové čerpadlo - oprava 2(1).xlsx",
    "docs/excel/02_Pomôcka - potreba tepla na vykurovanie(1).xlsx",
    "docs/excel/03_Pomôcka - bilancia VYK a TV(1).xlsx"
]

def inspect_file(filepath):
    print(f"\n--- Inspecting {filepath} ---")
    try:
        xl = pd.ExcelFile(filepath)
        print("Sheet names:", xl.sheet_names)
        for sheet in xl.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet, nrows=5)
            print(f"\nSheet: {sheet}")
            print(df.to_string())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

if __name__ == "__main__":
    inspect_file("docs/excel/03_Pomôcka - bilancia VYK a TV(1).xlsx")
