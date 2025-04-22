import streamlit as st
import pandas as pd
from feed_utils import fetch_multiple_feeds
from analysis_utils import analyse_and_store
from database import fetch_all_threats
from chromadb_utils import query_similar_threats
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import os

# Page and theme configuration
st.set_page_config(page_title="Hybrid Threat Intelligence Dashboard", layout="wide")
st.markdown("""
    <style>
        body { background-color: #121212; color: #e6e6e6; }
        .stButton>button { background-color: #7a04eb; color: white; }
        .stTextInput>div>div>input { background-color: #333333; color: #ffffff; }
        [data-testid="stExpander"] div[role="button"] { color: #ff005f; }
        .stDataFrame { background-color: #262730; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Hybrid Threat Intelligence Dashboard")

# Fetch & Analyse Latest Threats
if st.sidebar.button("Fetch & Analyse Latest Threats"):
    with st.spinner("Analysing threats..."):
        feeds = fetch_multiple_feeds([
            "https://feeds.feedburner.com/TheHackersNews",
            "https://threatpost.com/feed/"
        ])
        for entry in feeds:
            analyse_and_store(
                entry["title"],
                entry["content"],
                entry.get("source", "Unknown Source"),
                entry.get("URL", "No URL Provided")
            )
    st.sidebar.success("Analysis complete!")

# Structured Threat Database with sortable columns
st.subheader("🛡️ Structured Threat Database (SQLite)")
threats = fetch_all_threats()

structured_data = [{
    "Timestamp": threat.timestamp,
    "Title": threat.title,
    "Severity": threat.analysis.get("severity_level", "Unknown"),
    "Summary": threat.analysis.get("summary_impact", ""),
    "Source": threat.analysis.get("source_name", "No Source Provided"),
    "URL": threat.analysis.get("source_url", "No Source Provided"),

} for threat in threats]

structured_df = pd.DataFrame(structured_data)

# Streamlit: Displaying URL as clickable links
def clickable_link(url):
    if url and url != "No URL Provided":
        return f'<a href="{url}" target="_blank">🔗 Link</a>'
    return "N/A"


# Ensure 'URL' column exists before applying clickable links
if "URL" in structured_df.columns:
    structured_df["Source Link"] = structured_df["URL"].apply(clickable_link)
    df_display = structured_df.drop(columns=["URL"])
else:
    structured_df["Source Link"] = "N/A"
    df_display = structured_df




# st.subheader("Structured Threat Database (SQLite)")
st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

# Sortable Dataframe
sorted_df = structured_df.sort_values(by=st.selectbox("Sort Structured DB by", structured_df.columns), ascending=False)
st.dataframe(sorted_df, use_container_width=True)

# Semantic Search Section with sorting
st.subheader("🧠 Semantic Search (ChromaDB)")
query = st.text_input("🔍 Semantic threat search")

if query:
    results = query_similar_threats(query)
    if results['documents']:
        semantic_data = [{
            "Summary": doc,
            "Severity": metadata.get("severity_level", "Unknown"),
            "Confidence": metadata.get("confidence", "Unknown"),
            "Affected Sectors": ", ".join(metadata.get("affected_systems_sectors", [])),
            "CVEs": ", ".join(metadata.get("cve_references", [])),
        } for doc, metadata in zip(results['documents'][0], results['metadatas'][0])]

        semantic_df = pd.DataFrame(semantic_data)

        if not semantic_df.empty:
            sort_column = st.selectbox("Sort Semantic Search by", semantic_df.columns)
            sorted_semantic_df = semantic_df.sort_values(by=sort_column, ascending=False)
            st.dataframe(sorted_semantic_df, use_container_width=True)
        else:
            st.info("No data to display after semantic search.")
    else:
        st.info("No similar threats found.")


# Integrated Chatbot using ChromaDB and SQLite
st.subheader("🤖 Intelligent Chatbot")

@st.cache_resource
def init_chatbot():
    api_key = os.getenv("OPENAI_API_KEY")
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
    llm = ChatOpenAI(temperature=0.5, model='gpt-4o-mini', api_key=api_key)

    vector_store = Chroma(
        collection_name="threat_embeddings",
        embedding_function=embeddings_model,
        persist_directory="./chroma_db",
    )

    retriever = vector_store.as_retriever(search_kwargs={'k': 30})
    return llm, retriever

llm, retriever = init_chatbot()

if "history" not in st.session_state:
    st.session_state.history = []

user_query = st.text_input("Ask me about threats...", key="chatbot")

if user_query:
    docs = retriever.invoke(user_query)
    knowledge = "\n\n".join([doc.page_content for doc in docs])

    rag_prompt = f"""
    You are a cybersecurity assistant. Provide answers based ONLY on the provided knowledge, not internal knowledge.
    
    User's question: {user_query}
    
    Conversation history: {st.session_state.history}
    
    Provided knowledge: {knowledge}
    """

    with st.spinner("Thinking..."):
        response = llm.invoke(rag_prompt)
        st.session_state.history.append((user_query, response.content))
        st.write(response.content)

    if st.button("Clear Conversation"):
        st.session_state.history.clear()
