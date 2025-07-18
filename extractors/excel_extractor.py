import pandas as pd

def extract_text(path):
    text = ""
    xls = pd.ExcelFile(path)
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        text += df.astype(str).to_string(index=False) + "\n"
    return text