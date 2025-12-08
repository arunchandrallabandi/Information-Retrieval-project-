import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from bs4 import BeautifulSoup

# Load precomputed TF-IDF data
with open('tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('filenames.pkl', 'rb') as f:
    filenames = pickle.load(f)

PAGES_DIR = 'crawler/crawler/pages'

# Function to extract only visible text from HTML
def get_visible_text(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove unwanted tags
    for tag in soup(["script", "style", "meta", "link", "noscript", "header", "footer", "nav"]):
        tag.decompose()
    
    # Get visible text
    text = soup.get_text(separator=" ", strip=True)
    return text

# Prepare documents with visible text only
docs = []
for filename in filenames:
    file_path = os.path.join(PAGES_DIR, filename)
    docs.append(get_visible_text(file_path))

# Function to generate snippet with highlighted query
def get_snippet(text, query_words, snippet_len=60):
    text_lower = text.lower()
    positions = [text_lower.find(word.lower()) for word in query_words if text_lower.find(word.lower()) != -1]
    if not positions:
        return text[:snippet_len] + "..."
    pos = min(positions)
    start = max(pos - snippet_len // 2, 0)
    end = min(pos + snippet_len // 2, len(text))
    snippet = text[start:end]
    
    # Highlight all query words
    for word in query_words:
        snippet = re.sub(f"(?i)({re.escape(word)})", r"<mark>\1</mark>", snippet)
    return snippet + "..."

# Function to perform search
def search(query, top_k=10):
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_idx = np.argsort(sims)[::-1][:top_k]
    results = []
    for idx in top_idx:
        if sims[idx] > 0:
            snippet = get_snippet(docs[idx], query.split())
            results.append({
                'filename': filenames[idx],
                'score': sims[idx],
                'snippet': snippet
            })
    return results

# Function for auto-suggestions
def suggest(query, max_suggestions=5):
    query_lower = query.lower()
    suggestions = []
    for idx, doc_text in enumerate(docs):
        if query_lower in doc_text.lower():
            snippet = get_snippet(doc_text, query.split(), snippet_len=30)
            suggestions.append(f"{filenames[idx]}: {snippet}")
        if len(suggestions) >= max_suggestions:
            break
    return suggestions
