# Import libraries for normalizing and tokenizing
from unorderedMap import UnorderedMap
import nltk
from nltk.tokenize import word_tokenize
import re

# If not installed, download punkt for tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


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


# Get txt file and run it through preprocessing
file_path = 'docs/KJB.txt'
text = ''.join(readFile(file_path))
normalizedText = normalizeText(text)
tokens = tokenizeText(normalizedText)

# Adds tokens to an unordered map
umap = UnorderedMap()
for i in tokens:
    umap.insert(i)

# Prints the top 100 words
print(umap.getTop100())
