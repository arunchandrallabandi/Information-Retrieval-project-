import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

PAGES_DIR = os.path.join("crawler/crawler", "pages")
docs = []
filenames = []

for filename in sorted(os.listdir(PAGES_DIR)):
    path = os.path.join(PAGES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        docs.append(f.read())
        filenames.append(filename)

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(docs)

# Save index
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)
with open('filenames.pkl', 'wb') as f:
    pickle.dump(filenames, f)

print("TF-IDF index successfully built!")
print(f"Indexed documents: {len(filenames)}")
