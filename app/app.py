import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("netflix_titles.csv")

df = load_data()

st.set_page_config(
    page_title="🎬 Netflix Data Exploration",  # Change the title here
    page_icon="🖥️",  # Change the favicon here (you can use emoji or an image path)
    layout="wide",  # Optional: You can choose 'centered' or 'wide' layout
)

# Title
st.title("🎬 Netflix Data Exploration App")

# Sidebar filters
st.sidebar.header("Filter Options")
type_filter = st.sidebar.multiselect("Type", df['type'].unique(), default=df['type'].unique())
country_filter = st.sidebar.multiselect("Country", df['country'].dropna().unique(), default=df['country'].dropna().unique())
year_filter = st.sidebar.slider("Release Year", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2021))
genre_filter = st.sidebar.text_input("Genre Contains")

# Apply filters
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['release_year'].between(*year_filter)) &
    (df['listed_in'].str.contains(genre_filter, case=False, na=False))
]

st.markdown(f"### Showing {len(filtered_df)} results")

# Show data
st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'listed_in']])

# Chart: Type count
type_count = filtered_df['type'].value_counts().reset_index()
type_count.columns = ['type', 'count']  # Rename columns to 'type' and 'count'

st.subheader("Distribution of Types")
fig1 = px.pie(type_count, values='count', names='type', title='Movie vs TV Show')
st.plotly_chart(fig1)


# Chart: Releases by year
yearly = filtered_df.groupby('release_year').size().reset_index(name='count')
fig2 = px.bar(yearly, x='release_year', y='count', title='Titles Released Per Year')
st.plotly_chart(fig2)

# Top 10 Countries
top_countries = filtered_df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['country', 'count']  # Rename columns to 'country' and 'count'

fig3 = px.bar(top_countries, x='country', y='count', title='Top 10 Producing Countries')
st.plotly_chart(fig3)

