from flask import Flask, render_template, request
import nltk
import re
from nltk.tokenize import word_tokenize
from unorderedMap import UnorderedMap
from maxHeap import MaxHeap

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)

def preprocess_text():

    with open('docs/KJB.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.lower()
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)

    tokens = word_tokenize(text)

    return tokens

tokens = preprocess_text()

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
            top100 = umap.getTop100()
            top_words = top100[:n] 
        elif method == 'max_heap':
            heap = MaxHeap(tokens)
            top_n = heap.top_n(n)
            top_words = [(word, freq) for freq, word in top_n]

    return render_template('index.html', top_words=top_words, method=method, n=n)

if __name__ == '__main__':
    app.run(debug=True)
