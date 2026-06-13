import streamlit as st
import requests

st.set_page_config(page_title="News Dashboard", layout="wide")

st.title("📰 News Dashboard")

# -----------------------------
# API KEY (FROM SECRETS)
# -----------------------------
api_key = st.secrets.get("NEWS_API_KEY", None)

if not api_key:
    st.error("❌ API Key not found. Please add NEWS_API_KEY in .streamlit/secrets.toml")
    st.stop()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "🌍 Country",
    ["in", "us", "gb", "au", "ca", "de", "fr"]
)

category = st.sidebar.selectbox(
    "📂 Category",
    ["general", "business", "entertainment", "health", "science", "sports", "technology"]
)

keyword = st.sidebar.text_input("🔎 Keyword Search")

limit = st.sidebar.slider("📊 Number of Articles", 1, 50, 10)

# -----------------------------
# FETCH BUTTON
# -----------------------------
if st.button("🚀 Fetch News"):

    with st.spinner("Fetching latest news..."):

        # Default endpoint
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "country": country,
            "category": category,
            "pageSize": limit
        }

        # If keyword is given, switch endpoint
        if keyword:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": api_key,
                "q": keyword,
                "pageSize": limit,
                "sortBy": "publishedAt"
            }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            st.error("❌ Error fetching news")
            st.write(response.json())
        else:
            articles = response.json().get("articles", [])

            if not articles:
                st.warning("No articles found")
            else:
                st.success(f"Found {len(articles)} articles")

                for article in articles:
                    st.markdown("---")

                    st.subheader(article.get("title", "No Title"))
                    st.write(article.get("description", "No Description"))

                    if article.get("url"):
                        st.markdown(f"🔗 [Read Full Article]({article['url']})")

                    if article.get("urlToImage"):
                        st.image(article["urlToImage"], use_container_width=True)
