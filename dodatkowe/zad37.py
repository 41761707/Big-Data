import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def compute_text_file_signatures(documents):
    # Step 1: Preparing data
    vectorizer = CountVectorizer()
    word_frequency_matrix = vectorizer.fit_transform(documents)
    word_frequency_matrix = word_frequency_matrix.toarray()
    print(word_frequency_matrix)
    n = word_frequency_matrix.shape[1]
    M = np.random.rand(1024, n)  # Generating random vectors

    signatures = []

    # Step 2: Calculating cosine signatures
    for document in word_frequency_matrix:
        print(M)
        print(document)
        signature = np.dot(M,document)
        print(signature)
        signatures.append(signature)

    # Step 3: Returning results
    return signatures

# Example usage
documents = []

#files = ["Szekspir/hamlet.txt","Szekspir/KingLear.txt","Szekspir/Othello.txt","Szekspir/RomeoJuliet.txt"]
files = ["a.txt","b.txt"]

for file in files:
    f = open(file)
    documents.append(str(f.read()))
    f.close()
signatures = compute_text_file_signatures(documents)
print(signatures)
#similarity_matrix = cosine_similarity(signatures)
#print(similarity_matrix)
