# Import libraries for normalizing and tokenizing
from flask import Flask, render_template, request
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
def readFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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
def preprocessText(file_path):
    text = ''.join(readFile(file_path))
    normalizedText = normalizeText(text)
    tokens = tokenizeText(normalizedText)
    return tokens

# Preprocess tokens once for efficiency
file_path = 'docs/KJB.txt'
tokens = preprocessText(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    top_words = []
    method = 'unordered_map'
    n = 100

    if request.method == 'POST':
        method = request.form.get('method', 'unordered_map')
        n_input = request.form.get('n', '100')
        try:
            n = int(n_input)
            if n < 1:
                n = 1
            elif n > len(set(tokens)):
                n = len(set(tokens))
        except ValueError:
            n = 100

        if method == 'unordered_map':
            umap = UnorderedMap()
            for token in tokens:
                umap.insert(token)
            top_words = umap.getTop100()[:n]
        elif method == 'max_heap':
            heap = MaxHeap(tokens)
            top_n = heap.top_n(n)
            top_words = [(word, freq) for freq, word in top_n]

    return render_template('index.html', top_words=top_words, method=method, n=n)

if __name__ == '__main__':
    app.run(debug=True)
