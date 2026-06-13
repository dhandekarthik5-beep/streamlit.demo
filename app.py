import streamlit as st
import requests
from datetime import datetime

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -------------------------------
# API Configuration
# -------------------------------
API_KEY = st.secrets["NEWS_API_KEY"]
BASE_URL = "https://newsapi.org/v2/top-headlines"

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("📰 News Filters")

country = st.sidebar.selectbox(
    "Select Country",
    {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Australia": "au",
        "Canada": "ca",
        "Germany": "de",
        "France": "fr"
    }.keys()
)

country_code = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr"
}[country]

category = st.sidebar.selectbox(
    "Select Topic",
    [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=100,
    value=20
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="e.g. AI, Tesla, Cricket"
)

search_button = st.sidebar.button("🔍 Search News")

# -------------------------------
# Title
# -------------------------------
st.title("📰 Advanced News Dashboard")
st.markdown("Stay updated with the latest headlines worldwide.")

# -------------------------------
# Fetch News Function
# -------------------------------
def fetch_news():
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "category": category,
        "pageSize": article_count
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"Error {response.status_code}: Unable to fetch news."
        )
        return None

# -------------------------------
# Search News Function
# -------------------------------
def search_news(query):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": article_count,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"Error {response.status_code}: Search failed."
        )
        return None

# -------------------------------
# Get Data
# -------------------------------
data = None

if search_button:
    if keyword:
        data = search_news(keyword)
    else:
        data = fetch_news()
else:
    data = fetch_news()

# -------------------------------
# Display Articles
# -------------------------------
if data and data.get("articles"):

    st.success(
        f"Found {len(data['articles'])} articles"
    )

    for article in data["articles"]:

        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown")
        description = article.get("description", "")
        url = article.get("url", "#")
        image = article.get("urlToImage")
        published = article.get("publishedAt", "")

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if image:
                    st.image(image, use_container_width=True)

            with col2:
                st.subheader(title)

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                if description:
                    st.write(description)

                st.markdown(
                    f"[📖 Read Full Article]({url})"
                )

            st.divider()

else:
    st.warning("No news articles found.")
