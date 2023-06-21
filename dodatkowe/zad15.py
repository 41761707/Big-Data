import mmh3
import re
from bitarray import bitarray


def get_words(filename):
    book = open(filename, 'r', encoding='utf-8').read()
    book = book.lower()                                
    book = re.sub(r'[^a-z0-9]+', ' ', book)            
    return book.split()


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array =   bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        for seed in range(self.num_hashes):
            index = mmh3.hash(item, seed) % self.size
            self.bit_array[index] = 1

    def __contains__(self, item):
        for seed in range(self.num_hashes):
            index = mmh3.hash(item, seed) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


hamlet_words = get_words('Szekspir/hamlet.txt')
test_words = get_words('Szekspir/KingLear.txt')\
            + get_words('Szekspir/ulysses_chapter1.txt')\
            + get_words('Szekspir/ulysses_chapter2.txt')\
            + get_words('Szekspir/ulysses_chapter3.txt')
test_words = [w for w in test_words if w not in hamlet_words]

bloom_filter = BloomFilter(len(hamlet_words), 8)
for w in hamlet_words:
    bloom_filter.add(w)

cnt = 0
for w in hamlet_words:
    if w not in bloom_filter:
        cnt += 1
false_neg = cnt / len(hamlet_words)

false_cnt = 0
for w in test_words:
        if w in bloom_filter:
            false_cnt += 1
false_pos = cnt / len(test_words)


print(f"False negatives: {false_neg:.2f}")
print(f"False positives: {false_pos:.2f}")