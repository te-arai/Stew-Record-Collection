import pandas as pd

# Common filler words we ignore
STOPWORDS = {
    "the", "a", "an", "by", "of", "to", "in", "on", "for",
    "album", "albums", "record", "records", "lp", "lps",
    "show", "me", "my", "all", "find"
}

def extract_keywords(query: str):
    words = query.lower().split()
    return [w for w in words if w not in STOPWORDS]


def apply_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df

    keywords = extract_keywords(query)

    if not keywords:
        return df

    # Row matches only if ALL keywords appear somewhere in the row
    def row_matches(row):
        row_text = " ".join(row.astype(str).str.lower())
        return all(keyword in row_text for keyword in keywords)

    mask = df.apply(row_matches, axis=1)
    return df[mask]
