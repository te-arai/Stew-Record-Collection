import pandas as pd

def apply_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df

    query = query.lower()

    mask = df.apply(
        lambda row: row.astype(str).str.lower().str.contains(query).any(),
        axis=1
    )

    return df[mask]
