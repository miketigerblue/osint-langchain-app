import feedparser
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

# Fetch RSS feeds
def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    return [{"title": entry.title, "summary": entry.summary, "link": entry.link} for entry in feed.entries]

# Fetch data from VirusTotal API
def fetch_virustotal_data(ip):
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {}

# LangChain based summarisation & classification
def analyse_threat(summary):
    prompt = ChatPromptTemplate.from_template(
        """You are a cybersecurity AI assistant. Summarise and classify the following threat summary into:
        - Severity Level (Low, Medium, High, Critical)
        - Confidence (Low, Medium, High)
        - Recommended action in concise bullet points.

        Threat Summary: {summary}
        
        Provide your answer clearly formatted."""
    )
    chain = prompt | llm
    return chain.invoke({"summary": summary}).content
