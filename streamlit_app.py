import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
file_path = 'Athlete_events.xlsx'
df = pd.read_excel(file_path)

# Handle any potential missing values in the dataframe
df.dropna(subset=['NOC', 'Sport', 'Age', 'Medal'], inplace=True)

# Title of the app
st.title('Olympic Athletes Analysis')

# Sidebar for user input
st.sidebar.title("Filter Options")

# Convert NOC to country names using an example mapping (replace with a complete mapping)
noc_to_country = {
    'USA': 'United States',
    'GBR': 'United Kingdom',
    'CHN': 'China',
    'RUS': 'Russia',
    'GER': 'Germany',
    'AUS': 'Australia',
    # Add all other NOCs with their respective country names
}

# Add a full mapping for all NOCs from a reliable source or manually add the NOCs
df['Country'] = df['NOC'].map(noc_to_country)

# Handle missing country mappings
df['Country'] = df['Country'].fillna(df['NOC'])

# List of unique countries for selection, remove NaN values if any
country_list = df['Country'].dropna().unique()
country_list.sort()

# Sidebar for country selection
country = st.sidebar.selectbox('Select a Country', country_list)

# Filter data based on the selected country
filtered_data = df[df['Country'] == country]

# Introduction
st.markdown("""
## Introduction
This dashboard provides a comprehensive analysis of Olympic athletes' data. Use the sidebar to filter by country and sport, and explore various visualizations including age distribution, medal distribution, country participation, and more.
""")

# Sidebar for sport selection
sport_list = filtered_data['Sport'].dropna().unique()
sport = st.sidebar.selectbox('Select a Sport', sport_list)

# Filter data further based on the selected sport
filtered_data_sport = filtered_data[filtered_data['Sport'] == sport]

# Plotting - Histogram for Age Distribution
st.header(f"Age Distribution of Athletes in {sport}")
if not filtered_data_sport.empty:
    fig, ax = plt.subplots()
    sns.histplot(filtered_data_sport['Age'].dropna(), kde=True, ax=ax)
    ax.set_title(f'Age Distribution of Athletes in {sport} from {country}')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
else:
    st.warning(f"No data available for {sport} from {country}")

# Plotting - Pie Chart for Medal Distribution
st.header(f"Medal Distribution in {sport}")
if not filtered_data_sport['Medal'].dropna().empty:
    medal_counts = filtered_data_sport['Medal'].value_counts()
    fig_pie = px.pie(values=medal_counts.values, names=medal_counts.index, title=f'Medal Distribution in {sport} from {country}')
    st.plotly_chart(fig_pie)
else:
    st.warning(f"No medal data available for {sport} from {country}")

# Plotting - Line Graph for Number of Athletes over the Years
st.header(f"Number of Athletes Over the Years in {sport}")
if not filtered_data_sport.empty:
    year_counts = filtered_data_sport['Year'].value_counts().sort_index()
    fig_line = px.line(x=year_counts.index, y=year_counts.values, labels={'x': 'Year', 'y': 'Number of Athletes'}, title=f'Number of Athletes Over the Years in {sport} from {country}')
    st.plotly_chart(fig_line)
else:
    st.warning(f"No data available for {sport} from {country}")

