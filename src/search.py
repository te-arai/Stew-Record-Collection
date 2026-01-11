import pandas as pd
import os
import streamlit as st

def load_collection(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        st.error(f"❌ Could not find the file: `{path}`")
        st.stop()

    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Error loading Excel file: {e}")
        st.stop()
