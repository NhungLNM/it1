import streamlit as st
import pandas as pd
import math
import plotly.express as px  # Import plotly express

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',  # This is an emoji shortcode. Could be a URL too.
)

# Useful constants
MIN_YEAR = 1896
MAX_YEAR = 2016
# Plotting - Age Distribution Histogram
if not filtered_data.empty:
    fig, ax = plt.subplots()
    sns.histplot(filtered_data['Age'].dropna(), kde=True, ax=ax)
    ax.set_title(f'Age Distribution of Athletes in {sport}')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
