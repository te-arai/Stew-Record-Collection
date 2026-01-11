import streamlit as st
import pandas as pd
import math


def show_table(df: pd.DataFrame):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def show_cards(df: pd.DataFrame):
    """
    Display records as responsive cards in a grid layout.
    """
    # Decide how many cards per row; tweak if you like
    cards_per_row = 3

    # Reset index for safe iteration
    df = df.reset_index(drop=True)

    n_rows = math.ceil(len(df) / cards_per_row)

    for row_idx in range(n_rows):
        cols = st.columns(cards_per_row)

        for col_idx in range(cards_per_row):
            record_idx = row_idx * cards_per_row + col_idx
            if record_idx >= len(df):
                break

            row = df.iloc[record_idx]

            artist = row.get("Artist", "")
            title = row.get("Title", "")
            format_ = row.get("Format", "")
            genre = row.get("Genre", "")
            year = row.get("Released", "")
            label = row.get("Label", "")
            rating = row.get("Rating", "")

            with cols[col_idx]:
                st.markdown(
                    _build_card_html(
                        artist=artist,
                        title=title,
                        format_=format_,
                        genre=genre,
                        year=year,
                        label=label,
                        rating=rating,
                    ),
                    unsafe_allow_html=True,
                )


def _build_card_html(artist, title, format_, genre, year, label, rating) -> str:
    """
    Build a small HTML/CSS card for a single record.
    """
    # Optional rating display
    rating_str = f"<div style='margin-top:4px; font-size:0.9em; color:#f39c12;'>Rating: {rating}</div>" if rating not in ("", None) else ""

    return f"""
    <div style="
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px 12px 10px 12px;
        margin-bottom: 16px;
        background-color: #fafafa;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        min-height: 120px;
    ">
        <div style="font-weight: 600; font-size: 1.05em; margin-bottom: 4px;">
            {artist}
        </div>
        <div style="font-weight: 500; margin-bottom: 6px;">
            {title}
        </div>
        <div style="font-size: 0.9em; color: #555;">
            {format_} • {genre} • {year}
        </div>
        <div style="font-size: 0.9em; color: #777; margin-top: 4px;">
            {label}
        </div>
        {rating_str}
    </div>
    """
