import streamlit as st
import pandas as pd
import math
import html
import os
import re

# DEBUG: confirm this file is actually being loaded
print("DISPLAY.PY LOADED")


# ---------------------------------------------------------
# COVER ART HELPERS
# ---------------------------------------------------------

def normalise_filename(artist, title):
    """
    Convert artist + title into a safe, predictable filename.
    Handles extra spaces, unicode spaces, punctuation, etc.
    """
    text = f"{artist}_{title}".lower()
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text


def find_cover_image(artist, title):
    """
    Instead of checking local disk, we assume the image exists
    in the GitHub repo under assets/covers.
    We return the expected filename so we can build a GitHub URL.
    """
    filename = normalise_filename(artist, title)
    return f"{filename}.jpg"  # You can add PNG/WebP support later if needed


# ---------------------------------------------------------
# TABLE VIEW
# ---------------------------------------------------------

def show_table(df: pd.DataFrame):
    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# ---------------------------------------------------------
# CARD VIEW
# ---------------------------------------------------------

def show_cards(df: pd.DataFrame):
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
# CARD HTML BUILDER (GITHUB IMAGE VERSION)
# ---------------------------------------------------------

def _build_card_html(artist, title, format_, genre, year, label, rating) -> str:
    """
    Build a modern card with:
    - Accent colour strip
    - Soft background
    - Hover-lift animation
    - HTML escaping
    - Cover art loaded from GitHub
    """

    # Escape text
    artist_esc = html.escape(str(artist))
    title_esc = html.escape(str(title))
    format_esc = html.escape(str(format_))
    genre_esc = html.escape(str(genre))
    year_esc = html.escape(str(year))
    label_esc = html.escape(str(label))
    rating_esc = html.escape(str(rating))

    # Build GitHub raw URL
    filename = find_cover_image(artist, title)
    github_url = f"https://raw.githubusercontent.com/te-arai/Stew-Record-Collection/main/assets/covers/{filename}"

    # DEBUG: print the URL being used
    print("DEBUG GITHUB URL:", github_url)

    # Try loading the image
    cover_html = f"""
<img src="{github_url}" style="
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
