import pandas as pd
import sys

def dump_excel(filepath, outpath):
    # Read all sheets
    xls = pd.ExcelFile(filepath)
    with open(outpath, 'w', encoding='utf-8') as f:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            f.write(f"=== SHEET: {sheet_name} ===\n")
            f.write(df.to_string(index=False, header=False))
            f.write("\n\n")

if __name__ == "__main__":
    dump_excel(sys.argv[1], sys.argv[2])
