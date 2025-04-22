import streamlit as st
import pandas as pd
import json
from feed_utils import fetch_multiple_feeds
from analysis_utils import analyse_and_store
from database import fetch_all_threats
from chromadb_utils import query_similar_threats
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import os
import ast

# Page setup
st.set_page_config(page_title="🚀 Hybrid Threat Intelligence Dashboard", layout="wide")

# Enhanced Cyberpunk style
st.markdown("""
<style>
body, .stApp {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Roboto', sans-serif;
}
.stButton>button {
    background-color: #0288d1;
    color: white;
    border-radius: 8px;
    transition: 0.3s ease;
}
.stButton>button:hover {
    background-color: #01579b;
}
table.dataframe {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
}
table.dataframe th, table.dataframe td {
    border: 1px solid #333333;
    padding: 8px;
    text-align: left;
}
table.dataframe tr:hover {
    background-color: #263238;
}
.stExpanderHeader {
    background-color: #1c1c1c;
    color: #00e676;
    padding: 10px;
    border-radius: 5px;
}
[data-testid="stExpander"] div[role="button"] {
    font-size: 14px;
    color: #00e676;
}
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
            analyse_and_store(entry["title"], entry["content"], entry.get("source", "Unknown"), entry.get("url", "No URL Provided"))
    st.sidebar.success("Analysis complete!")

# Fetch threats from SQLite
threats = fetch_all_threats()

# Prepare structured threat data including extended JSON analysis fields
structured_data = [{
    "Timestamp": threat.timestamp,
    "Title": threat.title,
    "Severity": threat.analysis.get("severity_level", "Unknown"),
    "Confidence": threat.analysis.get("confidence", "Unknown"),
    "Source": threat.analysis.get("source_name", "Unknown Source"),
    "URL": threat.analysis.get("source_url", "No URL Provided"),
    "Recommended Actions": ", ".join(threat.analysis.get("recommended_actions", [])),
    "Key IOCs": ", ".join(threat.analysis.get("key_IOCs", [])),
    "Affected Sectors": ", ".join(threat.analysis.get("affected_systems_sectors", [])),
    "Mitigation Strategies": ", ".join(threat.analysis.get("mitigation_strategies", [])),
    "Potential Threat Actors": ", ".join(threat.analysis.get("potential_threat_actors", [])),
    "Historical Context": threat.analysis.get("historical_context", ""),
    "Summary Impact": threat.analysis.get("summary_impact", ""),
    "Relevance": threat.analysis.get("relevance", ""),
    "Additional Notes": threat.analysis.get("additional_notes", ""),
    "CVE References": ", ".join(threat.analysis.get("cve_references", [])),
    "Analysis": json.dumps(threat.analysis)  # Store entire JSON analysis
} for threat in threats]
structured_df = pd.DataFrame(structured_data)

# Add clickable links column
structured_df["Source Link"] = structured_df["URL"].apply(
    lambda url: f"[🔗 Link]({url})" if url != "No URL Provided" else "N/A"
)

# Drop the raw URL column from view
structured_df_display = structured_df.drop(columns=["URL"])

# Allow users to sort by any column
sort_column = st.selectbox("Sort threats by", structured_df_display.columns, index=0)
sorted_df = structured_df_display.sort_values(by=sort_column, ascending=False)

# Render DataFrame neatly using Streamlit's native dataframe for interactivity
st.dataframe(sorted_df, use_container_width=True)

# Expandable detailed JSON analysis sections with clean formatting
st.subheader("📄 Detailed Threat Analysis")
for idx, row in structured_df.iterrows():
    expander_title = f"{row['Timestamp']} - {row['Title']} [{row['Severity']}]"
    with st.expander(expander_title):
        st.json(json.loads(row["Analysis"]), expanded=False)

# Semantic Search Section
st.subheader("🧠 Semantic Search (ChromaDB)")
query = st.text_input("🔍 Enter semantic search query here")

if query:
    results = query_similar_threats(query)
    if results['documents']:
        semantic_data = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            affected_sectors = metadata.get("affected_systems_sectors", [])
            cve_references = metadata.get("cve_references", [])

            # Handle case where fields are stored as strings
            if isinstance(affected_sectors, str):
                affected_sectors = ast.literal_eval(affected_sectors)

            if isinstance(cve_references, str):
                cve_references = ast.literal_eval(cve_references)

            semantic_data.append({
                "Summary": doc,
                "Severity": metadata.get("severity_level", "Unknown"),
                "Confidence": metadata.get("confidence", "Unknown"),
                "Affected Sectors": ", ".join(affected_sectors),
                "CVEs": ", ".join(cve_references),
            })

        semantic_df = pd.DataFrame(semantic_data)

        st.dataframe(semantic_df, use_container_width=True)
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

    retriever = vector_store.as_retriever(search_kwargs={'k': 10})
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
        st.markdown(response.content)

    if st.button("Clear Conversation"):
        st.session_state.history.clear()
