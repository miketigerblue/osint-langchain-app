import streamlit as st
from feed_utils import fetch_multiple_feeds
from analysis_utils import analyze_article

# --- Configuration ---
st.set_page_config(page_title="OSINT Threat Analysis", layout="wide")
feed_urls = [
    "https://www.darkreading.com/rss.xml",
    "https://feeds.feedburner.com/TheHackersNews",
    #"https://threatpost.com/feed/",
    #"https://www.nist.gov/news-events/cybersecurity/rss.xml"
    # Add any other RSS/Atom feed URLs here
]

# --- App Title and Description ---
st.title("OSINT Threat Analysis Dashboard")
st.write("This app aggregates threat intelligence from RSS feeds and analyzes each item using LangChain + OpenAI.")

# --- Fetch RSS Feeds ---
with st.spinner("Fetching latest feeds..."):
    entries = fetch_multiple_feeds(feed_urls)

if not entries:
    st.error("No feed entries found. Please check the feed URLs or your internet connection.")
else:
    # Optionally, sort entries by date or filter as needed (not implemented here for simplicity)
    for entry in entries:
        title = entry["title"]
        content = entry["content"]
        if not content:
            # Skip entries with no content to analyze
            continue

        # Display the article title and a short preview
        st.subheader(title)
        if content:
            st.write(content[:200] + ("..." if len(content) > 200 else ""))

        # Analyze the article content using the LLM chain
        with st.spinner(f"Analyzing: {title[:50]}..."):
            analysis = analyze_article(title, content)
        # Display the analysis result
        st.markdown(f"**Threat Analysis:** {analysis}")

        st.markdown("---")  # separator between entries
