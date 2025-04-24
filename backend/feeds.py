import feedparser

def fetch_feed_entries(feed_url: str):
    """Parse a single RSS/Atom feed URL and return a list of entries with title and content."""
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries:
        title = entry.get('title', 'Untitled')
        # Determine content or summary field
        if 'content' in entry:
            # Some feeds use 'content' (which can be a list of parts)
            content_parts = [c.value for c in entry.content if hasattr(entry, 'content')]
            content = " ".join(content_parts).strip()
        else:
            # Fallback to summary or description if available
            content = entry.get('summary', entry.get('description', ''))
        entries.append({"title": title, "content": content})
    return entries

def fetch_multiple_feeds(feed_urls: list):
    """Fetch and parse multiple feeds, returning a combined list of entries."""
    all_entries = []
    for url in feed_urls:
        try:
            entries = fetch_feed_entries(url)
            all_entries.extend(entries)
        except Exception as e:
            print(f"Warning: failed to parse feed {url} – {e}")
    return all_entries
