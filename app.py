# Import libraries for normalizing and tokenizing
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from unorderedMap import UnorderedMap
from maxHeap import MaxHeap
import nltk
from nltk.tokenize import word_tokenize
import re
import os

# If not installed, download punkt for tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)

# Set upload folder and max file upload size to 8MB
app.config['UPLOAD_FOLDER'] = './docs'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

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

# Placeholders for file processing
tokens = []
pcHeap = None
pcTop100 = []
pcMap = None
pcUniqueWords = 0
totalWordCount = 0
currentFileName = "KJB.txt"

# Preprocess KJB.txt on startup as default
def preprocessKJB():
    global tokens, pcHeap, pcTop100, pcMap, pcUniqueWords, totalWordCount, currentFileName

    defaultFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'KJB.txt')

    tokens = preprocessText(defaultFilePath)
    totalWordCount = len(tokens)

    pcHeap = MaxHeap(tokens)
    pcTop100 = pcHeap.top_n(100)
    pcMap = initializeUnorderedMap(tokens)
    pcUniqueWords = pcMap.getSize()

# Call preprocessKJB() during app initialization
preprocessKJB()

# Handle file uploads and preprocessing
@app.route('/upload', methods=['POST'])
def upload():
    global tokens, pcHeap, pcTop100, pcMap, pcUniqueWords, totalWordCount, currentFileName

    # Ensure a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided: Please upload a .txt file'}), 400

    file = request.files['file']

    # Check if the file is a .txt file
    if not file.filename.endswith('.txt'):
        return jsonify({'error': 'Please only upload a .txt file'}), 400

    # Save the file
    currentFileName = secure_filename(file.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], currentFileName)
    file.save(filePath)

    # Preprocess the uploaded file
    tokens = preprocessText(filePath)
    totalWordCount = len(tokens)

    # Renew precomputed values
    pcHeap = MaxHeap(tokens)
    pcTop100 = pcHeap.top_n(100)
    pcMap = initializeUnorderedMap(tokens)
    pcUniqueWords = pcMap.getSize()

    return jsonify({'message': f'File uploaded successfully'})

# Display top 100 by default
@app.route('/')
def index():
    return render_template(
        'index.html',
        topWords=pcTop100,
        uniqueWordCount=pcUniqueWords,
        totalWordCount=totalWordCount,
        topWordsDataStructure="maxHeap",
        searchDataStructure="unorderedMap",
        searchQuery="",
        searchResult=None,
        currentFileName=currentFileName
    )

@app.route('/refresh', methods=['POST'])
def refresh():
    # Reinitialize map and heap based on config input
    topWordsDataStructure = request.json.get("topWordsDataStructure", "maxHeap")
    searchDataStructure = request.json.get("searchDataStructure", "unorderedMap")

    topWords = []
    uniqueWordCount = 0

    if topWordsDataStructure == "maxHeap":
        heap = MaxHeap(tokens)
        rawTopWords = heap.top_n(100)
        topWords = [(word, freq) for freq, word in rawTopWords]
        uniqueWordCount = len(set(tokens))
    elif topWordsDataStructure == "unorderedMap":
        umap = UnorderedMap()
        for token in tokens:
            umap.insert(token)
        rawTopWords = umap.getTop100()[:100]
        topWords = rawTopWords
        uniqueWordCount = umap.getSize()

    return jsonify({
        "topWords": topWords,
        "uniqueWordCount": uniqueWordCount,
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
