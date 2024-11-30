
# Blessed Carlo Acutis, ora pro nobis
class MaxHeap:
    pq = []
    tokens = []
    word_counts = dict()

    # initialized with all tokens

    def __init__(self, words):
        words_set = set()
        for word in words:
            words_set.add(word)
        for word in words_set:
            self.tokens.append(word)
        for word in words:
            if word not in self.word_counts:
                self.word_counts[word] = 0
            self.word_counts[word] += 1
        self.insert_all(self.tokens)

    def insert(self, word):
        pair = (self.word_counts[word], word)
        self.pq.append(pair)

        child = len(self.pq) - 1
        parent = (child - 1) // 2

        # heapify up

        while parent >= 0 and self.pq[parent][0] < self.pq[child][0]:
            temp = self.pq[child]
            self.pq[child] = self.pq[parent]
            self.pq[parent] = temp
            # self.pq[parent], self.pq[child] = self.pq[child], self.pq[parent]
            child = parent
            parent = (child - 1) // 2

    # used for testing
    def print_tokens(self):
        for token in self.pq:
            print(token)

    """
    def extract_copy(self, pq):
        print("extract_copy start")

        pq[0] = pq[-1]
        # pq[-1] = pq[0]
        extract = pq.pop()

        parent = 0
        left_child = 2 * parent + 1
        right_child = 2 * parent + 2

        # pq[parent] = pq[-1]

        # heapify down

        print("heapifying")
        while left_child < len(pq):
            parent_priority = pq[parent][0]
            left_child_priority = pq[left_child][0]

            if right_child < len(pq):
                right_child_priority = pq[right_child][0]
            else:
                right_child_priority = -1

            # print(f"parent: {parent}, left_child: {left_child}, right_child: {right_child}")
            # print(f"parent_priority: {parent_priority}, left_child_priority: {left_child_priority}, right_child_priority: {right_child_priority}")

            if left_child_priority > right_child_priority and left_child_priority > parent_priority:
                print("left bigger")
                # temp = pq[parent]
                # pq[parent] = pq[left_child]
                # pq[left_child] = temp
                pq[parent], pq[left_child] = pq[left_child], pq[parent]
                # print("before" + str(parent))
                parent = left_child
                # print("after" + str(parent))

            elif right_child_priority > left_child_priority and right_child_priority > parent_priority:
                print("right bigger")
                temp = pq[parent]
                # pq[parent] = pq[right_child]
                # pq[right_child] = temp
                # print("before" + str(parent))
                pq[parent], pq[right_child] = pq[right_child], pq[parent]
                parent = right_child
                # print("after" + str(parent))
            # the following elif condition breaks the function, not sure why. It works alright with else.
            # elif left_child_priority < parent_priority and right_child_priority < parent_priority:
            else:
                print("both smaller")
                break

            # print("parent now: " + str(parent))
            left_child = 2 * parent + 1
            right_child = 2 * parent + 2
            # print("update children")
        print("extract_copy done")
        return extract
    """

    def extract_copy(self, pq):
        if len(pq) == 0:
            print("Heap is empty.")
            return None

        # Replace root with the last element and pop the last element
        root = pq[0]
        pq[0] = pq[-1]
        pq.pop()

        parent = 0
        while True:
            left_child = 2 * parent + 1
            right_child = 2 * parent + 2
            largest = parent

            # Check if left child is larger
            if left_child < len(pq) and pq[left_child][0] > pq[largest][0]:
                largest = left_child

            # Check if right child is larger
            if right_child < len(pq) and pq[right_child][0] > pq[largest][0]:
                largest = right_child

            # If parent is the largest, stop heapifying
            if largest == parent:
                break

            # Swap parent with the largest child
            pq[parent], pq[largest] = pq[largest], pq[parent]
            parent = largest
        return root

    def insert_all(self, tokens):
        for token in tokens:
            self.insert(token)

    def search(self, token):
        """pq_copy = self.pq[:]
        while pq_copy:
            current = pq_copy.pop()
            if current[1] == token:
                return current
        return -1"""
        for pair in self.pq:
            if pair[1] == token:
                return pair
        return -1

    def top_n(self, n):
        top_n = []
        pq_copy = self.pq[:]
        if n > len(self.pq):
            n = len(self.pq)
        for i in range(n):
            top_n.append(self.extract_copy(pq_copy))
        return top_n

    def print_top_n(self, n):
        top_n = self.top_n(n)
        for pair in top_n:
             print(f"{pair[1]}: {pair[0]} \n")

