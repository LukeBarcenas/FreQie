# Import libraries for normalizing and tokenizing
from flask import Flask, render_template, request, jsonify
from unorderedMap import UnorderedMap
from maxHeap import MaxHeap
import nltk
from nltk.tokenize import word_tokenize
import re

# If not installed, download punkt for tokenization
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt/punkt_tab')

except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# Initialize Flask app
app = Flask(__name__)

# Reads a file line by line
def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        for line in file:
            yield line

# Normalizes the text by removing unwanted characters
def normalizeText(text):
    text = text.lower()
    text = re.sub(r'\d+', ' ', text)  # Removes numbers
    text = re.sub(r'[^\w\s]', '', text)  # Removes punctuation
    return text

# Tokenizes the text into words
def tokenizeText(text):
    tokens = word_tokenize(text)
    return tokens

# Preprocess the text
def preprocessText(filePath):
    text = ''.join(readFile(filePath))
    normalizedText = normalizeText(text)
    tokens = tokenizeText(normalizedText)
    return tokens

# Initializes the UnorderedMap
def initializeUnorderedMap(tokens):
    umap = UnorderedMap()
    for token in tokens:
        umap.insert(token)
    return umap

# Initializes the Heap
def initializeMaxHeap(tokens):
    return MaxHeap(tokens)

# Preprocess tokens once for efficiency
filePath = 'docs/KJB.txt'
tokens = preprocessText(filePath)

# Precompute once (Immutable)
pcHeap = MaxHeap(tokens)
pcTop100 = pcHeap.top_n(100)
pcMap = UnorderedMap()
for token in tokens:
    pcMap.insert(token)

# Display top 100 by default
@app.route('/')
def index():
    return render_template(
        'index.html',
        topWords=pcTop100,
        topWordsDataStructure="maxHeap",
        searchDataStructure="unorderedMap",
        searchQuery="",
        searchResult=None
    )

@app.route('/refresh', methods=['POST'])
def refresh():
    # Reinitializea  map and heap based on config input
    topWordsDataStructure = request.json.get("topWordsDataStructure", "maxHeap")
    searchDataStructure = request.json.get("searchDataStructure", "unorderedMap")

    topWords = []
    if topWordsDataStructure == "maxHeap":
        heap = MaxHeap(tokens)
        rawTopWords = heap.top_n(100)
        topWords = [(word, freq) for freq, word in rawTopWords]
    elif topWordsDataStructure == "unorderedMap":
        umap = UnorderedMap()
        for token in tokens:
            umap.insert(token)
        rawTopWords = umap.getTop100()[:100]
        topWords = rawTopWords

    return jsonify({
        "topWords": topWords,
        "searchDataStructure": searchDataStructure,
    })

# Searches precomputed map/heap depending on config
@app.route('/search', methods=['POST'])
def search():
    searchQuery = request.json.get("searchQuery", "").strip().lower()
    searchDataStructure = request.json.get("searchDataStructure", "unorderedMap")
    searchResult = None

    if searchDataStructure == "unorderedMap":
        try:
            searchResult = pcMap.search(searchQuery)
        except KeyError:
            searchResult = None
    elif searchDataStructure == "maxHeap":
        heap = MaxHeap(tokens)
        result = heap.search(searchQuery)
        if result != -1:
            searchResult = result[0]

    return jsonify({"searchQuery": searchQuery, "searchResult": searchResult})

if __name__ == '__main__':
    app.run(debug=True)
