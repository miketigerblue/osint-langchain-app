import feedparser
import logging
from datetime import datetime

def fetch_feed_entries(url: str):
    feed = feedparser.parse(url)
    source_name = feed.feed.get('title', 'Unknown Source')
    
    entries = []
    for entry in feed.entries:
        timestamp = entry.get("published_parsed") or entry.get("updated_parsed")
        if timestamp:
            timestamp = datetime(*timestamp[:6])
        else:
            timestamp = datetime.now()
        
        entries.append({
            "title": entry.get("title", "No Title"),
            "content": entry.get("summary", ""),
            "source": source_name,
            "URL": entry.get("link", "No URL Provided"),
            "timestamp": timestamp
        })

    return entries

def fetch_multiple_feeds(feed_urls: list):
    """Fetch and parse multiple feeds, returning combined entries sorted by timestamp."""
    all_entries = []
    for url in feed_urls:
        try:
            entries = fetch_feed_entries(url)
            logging.info(f"Fetched {len(entries)} entries from {url}")
            all_entries.extend(entries)
        except Exception as e:
            logging.error(f"Failed to parse feed {url}: {e}")

    # Sort entries by timestamp descending
    all_entries.sort(key=lambda x: x['timestamp'], reverse=True)
    return all_entries
