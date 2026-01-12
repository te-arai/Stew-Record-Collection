import streamlit as st
import pandas as pd
import math
import html
import os
import re


# ---------------------------------------------------------
# COVER ART HELPERS
# ---------------------------------------------------------

def normalise_filename(artist, title):
    """
    Convert artist + title into a safe, predictable filename.
    Example:
        "A Flock Of Seagulls", "Telecommunication"
        → "a_flock_of_seagulls_telecommunication"
    """
    text = f"{artist}_{title}".lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)   # replace non-alphanumerics
    text = re.sub(r"_+", "_", text).strip("_")  # collapse underscores
    return text


def find_cover_image(artist, title, base_path="assets/covers"):
    """
    Look for a matching cover image in the assets/covers directory.
    Supports jpg, jpeg, png, webp.
    Returns a file path or None.
    """
    base = normalise_filename(artist, title)

    for ext in ["jpg", "jpeg", "png", "webp"]:
        path = os.path.join(base_path, f"{base}.{ext}")
        if os.path.exists(path):
            return path

    return None


# ---------------------------------------------------------
# TABLE VIEW
# ---------------------------------------------------------

def show_table(df: pd.DataFrame):
    """
    Display the dataframe in a clean, wide table.
    """
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# CARD VIEW
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# CARD HTML BUILDER (WITH COVER ART)
# ---------------------------------------------------------

def _build_card_html(artist, title, format_, genre, year, label, rating) -> str:
    """
    Build a modern card with:
    - Accent colour strip
    - Soft background
    - Hover-lift animation (CSS class: record-card)
    - HTML escaping for all text fields
    - Optional cover art if available
    """

    # Escape text
    artist_esc = html.escape(str(artist))
    title_esc = html.escape(str(title))
    format_esc = html.escape(str(format_))
    genre_esc = html.escape(str(genre))
    year_esc = html.escape(str(year))
    label_esc = html.escape(str(label))
    rating_esc = html.escape(str(rating))

    # Try to find cover art
    cover_path = find_cover_image(artist, title)
    cover_html = ""
    if cover_path:
        cover_html = f"""
<img src="file://{cover_path}" style="
    width: 100%;
    border-radius: 6px;
    margin-bottom: 10px;
">
"""

    rating_str = (
        f"<div style='margin-top:6px; font-size:0.9em; color:#e67e22;'>Rating: {rating_esc}</div>"
        if rating_esc not in ("", None, "nan")
        else ""
    )

    # IMPORTANT: no indentation, no leading newline
    return f"""<div class="record-card" style="
border: 1px solid #ddd;
border-left: 6px solid #e67e22;
border-radius: 6px;
padding: 14px;
margin-bottom: 18px;
background-color: #fff8f0;
box-shadow: 0 1px 3px rgba(0,0,0,0.1);
min-height: 130px;
">

{cover_html}

<div style="font-weight: 600; font-size: 1.1em; margin-bottom: 4px;">
    {artist_esc}
</div>

<div style="font-weight: 500; margin-bottom: 6px;">
    {title_esc}
</div>

<div style="font-size: 0.9em; color: #555;">
    {format_esc} • {genre_esc} • {year_esc}
</div>

<div style="font-size: 0.85em; color: #777; margin-top: 4px;">
    {label_esc}
</div>

{rating_str}

</div>"""
