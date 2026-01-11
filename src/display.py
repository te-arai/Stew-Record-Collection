import streamlit as st
import pandas as pd

def show_table(df: pd.DataFrame):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
