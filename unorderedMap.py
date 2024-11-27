class UnorderedMap:
    def __init__(self):
        # Start with 128 buckets
        self.buckets = []
        for i in range(128):
            self.buckets.append([])

        self.mapSize = 0
        self.loadFactorThreshold = 0.75

    # Makes a hash value for the key with the ASCII 31 power method
    def makeHash(self, key):
        bucketCount = len(self.buckets)
        hashValue = 0

        # Update hash by multiplying 31 for each letter and add the ascii
        # value for uniqueness for different letter arrangements
        for i in key:
            hashValue = (hashValue * 31 + ord(i)) % bucketCount
        return hashValue

    # Creates/Increments the specified key by 1
    def insert(self, key):
        # Resize map if load factor passes threshold
        if self.mapSize / len(self.buckets) > self.loadFactorThreshold:
            self.resizeBuckets()

        # Get the hash index of the key and go to the bucket
        index = self.makeHash(key)
        bucket = self.buckets[index]

        # Go through the bucket and see if the key is there, if so, increment frequency
        for i, (tempKey, frequency) in enumerate(bucket):
            if tempKey == key:
                bucket[i] = (key, frequency + 1)
                return

        # If key is not found, add it and increment frequency
        bucket.append((key, 1))
        self.mapSize += 1

    # Find the value for a specific key
    def search(self, key):
        # Get the hash index of the key and go to the bucket
        index = self.makeHash(key)
        bucket = self.buckets[index]

        # Look for the key in the bucket, if its there, return the frequency
        for tempKey, frequency in bucket:
            if tempKey == key:
                return frequency
        # If a keyError is raised, state that the key doesn't exist
        raise KeyError(f"'{key}' is not in this text")

    # Resizes the map and rehashes (is called when the load factor threshold is exceeded)
    def resizeBuckets(self):
        # Keep the old buckets for rehashing, double the bucket count for new size,
        # and set the map size to 0 for reinserting
        oldBuckets = self.buckets
        self.buckets = [[] for i in range(len(oldBuckets) * 2)]
        self.mapSize = 0

        # Refill buckets
        for bucket in oldBuckets:
            for tempKey, frequency in bucket:
                for i in range(frequency):
                    self.insert(tempKey)

    # Prints out all keys and frequencies (unordered)
    def printMap(self):
        for i in self.buckets:
            for key, frequency in i:
                print(f"({key}: {frequency})")

    # Returns the amount of unique words in the map
    def getSize(self):
        return self.mapSize

    # Gets the top 100 words in the map (O(n) complexity)
    def getTop100(self):
        topWords = []

        for i in range(100):
            # Hold the key with the largest value, the largest value that the key has,
            # the bucket where the key is, and the index of the key in the bucket
            maxKey = None
            maxValue = -1
            maxBucket = None
            maxIndex = -1

            # Search the whole map for the maximum value, changing the maxVariables if needed
            for i in self.buckets:
                for j, (key, value) in enumerate(i):
                    if value > maxValue:
                        maxKey, maxValue = key, value
                        maxBucket, maxIndex = i, j

            # If no key was found, break
            if maxKey is None:
                break

            # Add the max key-value pair to topWords
            topWords.append((maxKey, maxValue))

            # Remove the max key-value pair to not get it again
            del maxBucket[maxIndex]

        return topWords
