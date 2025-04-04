import pandas as pd
from utils import fetch_rss_feed, analyse_threat

RSS_URLS = [
    "https://www.darkreading.com/rss.xml",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://threatpost.com/feed/"
]

def ingest_and_analyse():
    threats = []
    for url in RSS_URLS:
        entries = fetch_rss_feed(url)
        for entry in entries:
            analysis = analyse_threat(entry["summary"])
            threats.append({
                "title": entry["title"],
                "link": entry["link"],
                "analysis": analysis
            })
    df = pd.DataFrame(threats)
    df.to_csv('cyber_threats.csv', index=False)
    print("Data saved successfully!")

if __name__ == "__main__":
    ingest_and_analyse()
