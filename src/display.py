import streamlit as st
import pandas as pd
import math
import html


def show_table(df: pd.DataFrame):
    """
    Display the dataframe in a clean, wide table.
    """
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def show_cards(df: pd.DataFrame):
    """
    Display records as responsive cards in a grid layout.
    Cards use a coloured accent strip and support hover-lift animation.
    """
    cards_per_row = 3
    df = df.reset_index(drop=True)
    n_rows = math.ceil(len(df) / cards_per_row)

    for row_idx in range(n_rows):
        cols = st.columns(cards_per_row)

        for col_idx in range(cards_per_row):
            record_idx = row_idx * cards_per_row + col_idx
            if record_idx >= len(df):
                break

            row = df.iloc[record_idx]

            with cols[col_idx]:
                st.markdown(
                    _build_card_html(
                        artist=row.get("Artist", ""),
                        title=row.get("Title", ""),
                        format_=row.get("Format", ""),
                        genre=row.get("Genre", ""),
                        year=row.get("Released", ""),
                        label=row.get("Label", ""),
                        rating=row.get("Rating", ""),
                    ),
                    unsafe_allow_html=True,
                )


def _build_card_html(artist, title, format_, genre, year, label, rating) -> str:
    """
    Build a modern card with:
    - Accent colour strip
    - Soft background
    - Hover-lift animation (CSS class: record-card)
    - HTML escaping for all text fields
    """

    # Escape all text to prevent HTML breakage
    artist = html.escape(str(artist))
    title = html.escape(str(title))
    format_ = html.escape(str(format_))
    genre = html.escape(str(genre))
    year = html.escape(str(year))
    label = html.escape(str(label))
    rating = html.escape(str(rating))

    rating_str = (
        f"<div style='margin-top:6px; font-size:0.9em; color:#e67e22;'>Rating: {rating}</div>"
        if rating not in ("", None, "nan")
        else ""
    )

    return f"""
    <div class="record-card" style="
        border: 1px solid #ddd;
        border-left: 6px solid #e67e22;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 18px;
        background-color: #fff8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        min-height: 130px;
    ">
        <div style="font-weight: 600; font-size: 1.1em; margin-bottom: 4px;">
            {artist}
        </div>

        <div style="font-weight: 500; margin-bottom: 6px;">
            {title}
        </div>

        <div style="font-size: 0.9em; color: #555;">
            {format_} • {genre} • {year}
        </div>

        <div style="font-size: 0.85em; color: #777; margin-top: 4px;">
            {label}
        </div>

        {rating_str}
    </div>
    """
