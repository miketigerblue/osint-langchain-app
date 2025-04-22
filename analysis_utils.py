import json
import uuid
from chromadb_utils import store_analysis_vector
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from database import save_threat_metadata
from datetime import datetime

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0, max_retries=5, request_timeout=60)

prompt_template = """
You're a cybersecurity analyst. Analyse the article and respond strictly in JSON, matching this schema:

{{
  "severity_level": "Low | Medium | High | Critical",
  "confidence": "Low | Medium | High",
  "recommended_actions": ["Action1", "Action2"],
  "key_IOCs": ["IOC1", "IOC2"],
  "affected_systems_sectors": ["Sector1", "Sector2"],
  "mitigation_strategies": ["Strategy1", "Strategy2"],
  "potential_threat_actors": ["Actor1", "Actor2"],
  "historical_context": "Brief historical context",
  "summary_impact": "Brief summary of threat impact",
  "relevance": "Relevance to cybersecurity landscape",
  "additional_notes": "Additional insights or notes",
  "cve_references": ["CVE-XXXX-XXXX"]
}}

Title: {title}
Content: {content}

IMPORTANT: Respond ONLY with the JSON object described above.
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
parser = JsonOutputParser()

analysis_chain = prompt | llm | parser

def analyse_and_store(title: str, content: str, source: str = "Unknown", url: str = "No URL Provided"):
    try:
        # Perform LLM-based analysis
        analysis_result = analysis_chain.invoke({"title": title, "content": content})

        # Generate a unique ID for ChromaDB storage
        document_id = str(uuid.uuid4())

        # Add source metadata explicitly to analysis result
        analysis_result["source_name"] = source
        analysis_result["source_url"] = url

        # Store threat metadata in SQLite (passing analysis_result only, as it already includes source metadata)
        save_threat_metadata(title, content, analysis_result)

        # Store embeddings in ChromaDB (analysis_result already contains source metadata)
        store_analysis_vector(document_id, analysis_result, source, url)

        return analysis_result

    except Exception as err:
        error_msg = {"error": str(err)}
        print("LLM Error:", error_msg)
        return error_msg

