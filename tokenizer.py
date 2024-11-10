# Import libraries for normalizing and tokenizing
import re
import ssl
import nltk
from nltk.tokenize import word_tokenize

# Set the certificate
ssl._create_default_https_context = ssl._create_unverified_context

# If not installed, download punkt for tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


# Reads a file line by line
def read_large_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line


# Normalizes text by removing unwanted characters
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\d+', ' ', text)  # Removes numbers
    text = re.sub(r'[^\w\s]', '', text)  # Removes punctuation
    return text


# Tokenizes the text into words
def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens


# Get txt file and run it through preprocessing
file_path = 'docs/KJB.txt'

text = ''.join(read_large_file(file_path))

normalized_text = normalize_text(text)

tokens = tokenize_text(normalized_text)

# Test with Counter to see if it works
from collections import Counter

word_counts = Counter(tokens)
top_100_words = word_counts.most_common(100)
print(top_100_words)
