import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# Load the data
file_path = 'Athlete_events.xlsx'
df = pd.read_excel(file_path)

# Title of the app
st.title('Olympic Athletes Analysis')

# Sidebar for user input
sport = st.sidebar.selectbox('Select a Sport', df['Sport'].unique())

# Useful constants
MIN_YEAR = 1896
MAX_YEAR = 2016

# Function to get GDP data
def get_gdp_data():
    # Assuming raw_gdp_df is already loaded with the data
    # For example:
    raw_gdp_df = pd.read_csv('gdp_data.csv')  # Replace with actual data source

    # Pivot the data
    gdp_df = raw_gdp_df.melt(
        id_vars=['Country Code'],
        value_vars=[str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        var_name='Year',
        value_name='GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

# Get GDP data
gdp_df = get_gdp_data()

# Set the title that appears at the top of the page.
st.markdown('''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
''')

# Add some spacing
st.text('')
st.text('')

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value]
)

countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
)

st.text('')
st.text('')
st.text('')

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries)) &
    (gdp_df['Year'] <= to_year) &
    (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

st.text('')
st.text('')

first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

st.text('')

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
