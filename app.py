import streamlit as st
from news_api import fetch_news
from summarizer import summarize_news

st.set_page_config(page_title="News Summarizer", layout="centered")
st.title("📰 Personalized News Summarizer")

tone = st.selectbox("Choose your preferred tone:", ["casual", "professional", "funny", "technical"])
category = st.selectbox("News Category:", ["business", "technology", "sports", "entertainment", "general"])

if st.button("Get News & Summarize"):
    with st.spinner("Fetching and summarizing..."):
        news_items = fetch_news(category=category, max_items=10)

        for item in news_items:
            st.subheader(item["title"])
            # summary = summarize_news(item["description"] or item["title"], tone=tone)
            summary = summarize_news(item["description"] or item["title"], tone=tone)

# Remove any lines with "<think>" or similar patterns
            clean_summary = "\n".join(
                line for line in summary.split("\n") if not line.strip().startswith("<")
            )
            st.write(clean_summary)
            st.markdown(f"[Read more]({item['websiteUrl']})")
