import streamlit as st
import pandas as pd
import os

from src.data_loader import load_collection
from src.search import apply_search
from src.display import show_table


# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="My Vinyl Collection",
    layout="wide",
)


# -----------------------------
# Load Dataset
# -----------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "record_collection.xlsx")
df = load_collection(DATA_PATH)

st.title("🎵 My Vinyl Record Collection")
st.markdown("Search, browse, and explore your entire vinyl library.")


# -----------------------------
# Global Search Bar
# -----------------------------
search_query = st.text_input(
    "Search your collection",
    placeholder="Try: 'ABC', 'albums by ABC', '1983 electronic', '12 inch singles'..."
)

filtered_df = apply_search(df, search_query)


# -----------------------------
# Display Table
# -----------------------------
show_table(filtered_df)
