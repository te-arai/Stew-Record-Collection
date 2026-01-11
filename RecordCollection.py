import streamlit as st
import pandas as pd
import os

from src.data_loader import load_collection
from src.search import apply_search
from src.display import show_table, show_cards


st.set_page_config(
    page_title="My Vinyl Collection",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "record_collection.xlsx")
df = load_collection(DATA_PATH)

st.title("🎵 My Vinyl Record Collection")
st.markdown("Search, filter, and explore your entire vinyl library.")


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

artists = ["All Artists"] + sorted(df["Artist"].dropna().unique().tolist())
artist_filter = st.sidebar.selectbox("Artist", artists)

formats = ["All Formats"] + sorted(df["Format"].dropna().unique().tolist())
format_filter = st.sidebar.selectbox("Format", formats)

genres = ["All Genres"] + sorted(df["Genre"].dropna().unique().unique().tolist())
genre_filter = st.sidebar.selectbox("Genre", genres)

years = sorted(df["Released"].dropna().unique().tolist())
year_filter = st.sidebar.multiselect("Year", years, default=[])


# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if artist_filter != "All Artists":
    filtered_df = filtered_df[filtered_df["Artist"] == artist_filter]

if format_filter != "All Formats":
    filtered_df = filtered_df[filtered_df["Format"] == format_filter]

if genre_filter != "All Genres":
    filtered_df = filtered_df[filtered_df["Genre"] == genre_filter]

if year_filter:
    filtered_df = filtered_df[filtered_df["Released"].isin(year_filter)]


# -----------------------------
# Search
# -----------------------------
search_query = st.text_input(
    "Search your collection",
    placeholder="Try: 'ABC', 'albums by ABC', '1983 electronic', '12 inch singles'..."
)

searched_df = apply_search(filtered_df, search_query)


# -----------------------------
# View Mode
# -----------------------------
view_mode = st.radio(
    "View mode",
    options=["Table", "Card"],
    horizontal=True,
)


# -----------------------------
# Display
# -----------------------------
if searched_df.empty:
    st.info("No records match your current filters/search.")
else:
    if view_mode == "Table":
        show_table(searched_df)
    else:
        show_cards(searched_df)
