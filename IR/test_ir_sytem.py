import requests
from bs4 import BeautifulSoup

BASE = "http://127.0.0.1:5000"

results = {}

def test_search():
    """Test basic search functionality."""
    try:
        r = requests.post(BASE + "/", data={"query": "information"})
        if r.status_code == 200:
            results["Search Functionality"] = "PASS — Search endpoint responded with status 200 OK."
        else:
            results["Search Functionality"] = f"FAIL — Unexpected status code {r.status_code}."
    except Exception as e:
        results["Search Functionality"] = f"FAIL — Exception occurred: {e}"

def test_snippet_highlighting():
    """Check if search snippets highlight query terms correctly."""
    try:
        r = requests.post(BASE + "/", data={"query": "data"})
        soup = BeautifulSoup(r.text, "html.parser")
        mark = soup.find("mark")
        if mark:
            results["Snippet Highlighting"] = f"PASS — Found highlighted snippet: '{mark.text}'."
        else:
            results["Snippet Highlighting"] = "FAIL — No <mark> tag found for query term."
    except Exception as e:
        results["Snippet Highlighting"] = f"FAIL — Exception occurred: {e}"

def test_auto_suggestion():
    """Verify that the auto-suggestion API returns suggestions for partial queries."""
    try:
        r = requests.get(BASE + "/suggest?q=inf")
        json_data = r.json()
        if len(json_data) > 0:
            results["Auto-Suggestion"] = f"PASS — Received {len(json_data)} suggestion(s) for 'inf'."
        else:
            results["Auto-Suggestion"] = "FAIL — No suggestions returned for partial query 'inf'."
    except Exception as e:
        results["Auto-Suggestion"] = f"FAIL — Exception occurred: {e}"

def test_empty_suggestion():
    """Verify that empty input returns no suggestions."""
    try:
        r = requests.get(BASE + "/suggest?q=")
        json_data = r.json()
        if json_data == []:
            results["Auto-Suggestion (Empty Input)"] = "PASS — Empty input returned empty suggestion list."
        else:
            results["Auto-Suggestion (Empty Input)"] = f"FAIL — Expected empty list, got {json_data}."
    except Exception as e:
        results["Auto-Suggestion (Empty Input)"] = f"FAIL — Exception occurred: {e}"

def test_read_more_links():
    """Check if 'Read More' links are present and valid."""
    try:
        r = requests.post(BASE + "/", data={"query": "web"})
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all("a", string=lambda x: "Read More" in x)
        if not links:
            results["Read More Links"] = "FAIL — No 'Read More' links found in search results."
        else:
            link = links[0]["href"]
            page = requests.get(BASE + link)
            if page.status_code == 200:
                results["Read More Links"] = f"PASS — 'Read More' link '{link}' accessible (status 200)."
            else:
                results["Read More Links"] = f"FAIL — 'Read More' link '{link}' returned status {page.status_code}."
    except Exception as e:
        results["Read More Links"] = f"FAIL — Exception occurred: {e}"

def test_multiple_queries():
    """Test system stability with multiple queries in sequence."""
    try:
        queries = ["ai", "analysis", "robotics", "cloud", "systems"]
        for q in queries:
            r = requests.post(BASE + "/", data={"query": q})
            if r.status_code != 200:
                results["Multiple Query Stability"] = f"FAIL — Query '{q}' returned status {r.status_code}."
                return
        results["Multiple Query Stability"] = f"PASS — All {len(queries)} queries returned status 200."
    except Exception as e:
        results["Multiple Query Stability"] = f"FAIL — Exception occurred: {e}"

def test_rare_words():
    """Check handling of rare/uncommon search terms."""
    try:
        rare = "xylophonometric"
        r = requests.post(BASE + "/", data={"query": rare})
        if r.status_code == 200:
            results["Rare Word Handling"] = f"PASS — Rare word '{rare}' handled successfully (status 200)."
        else:
            results["Rare Word Handling"] = f"FAIL — Rare word '{rare}' returned status {r.status_code}."
    except Exception as e:
        results["Rare Word Handling"] = f"FAIL — Exception occurred: {e}"

# ---------- RUN TESTS ----------
test_search()
test_snippet_highlighting()
test_auto_suggestion()
test_empty_suggestion()
test_read_more_links()
test_multiple_queries()
test_rare_words()

print("\n========== INFORMATION RETRIEVAL SYSTEM TEST REPORT ==========\n")
for key, value in results.items():
    print(f"{key}: {value}")

print("\nTest Run Completed.\n")
