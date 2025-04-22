import streamlit as st
import pandas as pd
from database import fetch_all_threats
import json

# Page setup
st.set_page_config(page_title="🌐 Daily Cyber Threat Analysis", layout="wide")

# Custom styles
st.markdown("""
<style>
    body, .stApp { background-color: #0e1117; color: #ffffff; font-family: Arial, sans-serif; }
    .threat-container { padding: 15px; border-radius: 8px; margin-bottom: 20px; background-color: #161b22; }
    h2 { color: #58a6ff; }
    .severity-high, .severity-critical { color: #ff3860; }
    .severity-medium { color: #ffdd57; }
    .severity-low { color: #23d160; }
    .source-link { text-decoration: none; color: #58a6ff; font-weight: bold; }
    .source-link:hover { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Daily Cyber Threat Analysis")

# Fetch threats
threats = fetch_all_threats()

# Display threats neatly
for threat in threats:
    analysis = threat.analysis
    severity = analysis.get("severity_level", "Unknown").lower()
    severity_class = f"severity-{severity}"
    timestamp = pd.to_datetime(threat.timestamp).strftime('%Y-%m-%d %H:%M')

    st.markdown(f"""
    <div class="threat-container">
        <h2>{threat.title}</h2>
        <p><strong>Timestamp:</strong> {timestamp}</p>
        <p><strong>Severity:</strong> <span class="{severity_class}">{analysis.get("severity_level", "Unknown")}</span></p>
        <p><strong>Confidence:</strong> {analysis.get("confidence", "Unknown")}</p>
        <p><strong>Summary Impact:</strong> {analysis.get("summary_impact", "")}</p>
        <p><strong>Affected Sectors:</strong> {', '.join(analysis.get("affected_systems_sectors", []))}</p>
        <p><strong>Recommended Actions:</strong> {', '.join(analysis.get("recommended_actions", []))}</p>
        <p><strong>Key IOCs:</strong> {', '.join(analysis.get("key_IOCs", []))}</p>
        <p><strong>Potential Threat Actors:</strong> {', '.join(analysis.get("potential_threat_actors", []))}</p>
        <p><strong>Mitigation Strategies:</strong> {', '.join(analysis.get("mitigation_strategies", []))}</p>
        <p><strong>CVE References:</strong> {', '.join(analysis.get("cve_references", []))}</p>
        <p><strong>Source:</strong> <a class="source-link" href="{analysis.get("source_url", "#")}" target="_blank">{analysis.get("source_name", "Unknown Source")}</a></p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
*Powered by [Your Company or Project Name]. Contact us at [your email].*
""")
