import streamlit as st
import pandas as pd
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
df = load_collection("data/record_collection.xlsx")

st.title("🎵 My Vinyl Record Collection")
st.markdown("Search, browse, and explore your entire vinyl library.")


# -----------------------------
# Global Search Bar
# -----------------------------
search_query = st.text_input(
    "Search your collection",
    placeholder="Try: 'Benson', '1983', '12\" Single', 'Electronic', 'CBS'..."
)

filtered_df = apply_search(df, search_query)


# -----------------------------
# Display Table
# -----------------------------
show_table(filtered_df)


