from flask import Flask, render_template, request, jsonify, send_from_directory
from query import search, suggest
import os

app = Flask(__name__)
PAGES_DIR = os.path.join("crawler", "crawler", "pages")

@app.route("/", methods=["GET", "POST"])
def index():
    query_text = ""
    results = []
    if request.method == "POST":
        query_text = request.form.get("query", "")
        results = search(query_text, top_k=12)
    return render_template("index.html", query=query_text, results=results)

@app.route("/suggest", methods=["GET"])
def suggest_route():
    q = request.args.get("q", "")
    suggestions = suggest(q) if q else []
    return jsonify(suggestions)

# Route to serve the actual HTML pages
@app.route("/page/<path:filename>")
def serve_page(filename):
    return send_from_directory(PAGES_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
