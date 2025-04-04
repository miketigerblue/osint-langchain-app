import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cyber Threat Intelligence Dashboard")

st.title("🌐 Real-Time OSINT Cyber Threat Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('cyber_threats.csv')
    return df

data = load_data()

st.sidebar.header("Filters")

search_query = st.sidebar.text_input("Search threats", "")

filtered_data = data[data['title'].str.contains(search_query, case=False)]

st.metric(label="Total Threats Ingested", value=len(data))

for idx, row in filtered_data.iterrows():
    st.subheader(f"🔺 {row['title']}")
    st.markdown(row['analysis'], unsafe_allow_html=True)
    st.markdown(f"[Read more here]({row['link']})")

st.caption("Dashboard updated weekly based on ingested OSINT data.")
