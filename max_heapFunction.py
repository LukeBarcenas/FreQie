import heapq

# function that creates a max heap given input

def maxHeap(tokens, word_counts):
    max_heap = []
    for token in tokens:
        word_counts[token] *= -1
        heapq.heappush(max_heap, (word_counts[token] * -1, token))
    return max_heap

# finds a given token by iterating through the heap

def searchHeap(max_heap, token):
    while max_heap:
        current = heapq.pop(max_heap)
        if current == token:
            return current

# finds first n number of tokens

def topHeap(max_heap, n):
    topN = []
    for i in range(n):
        topN.append(heapq.pop(max_heap))
    return topN


