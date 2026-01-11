import pandas as pd

def load_collection(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()  # Clean column names
    return df
