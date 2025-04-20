# summarizer.py

def summarize(text):
    # This is a mock version — we'll use real summarization later
    if len(text) < 100:
        return text
    return text[:300] + "..."  # Return the first 300 characters as a fake summary
