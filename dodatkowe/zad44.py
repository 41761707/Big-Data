import numpy as np
import matplotlib.pyplot as plt

def generate_distances(k, n):
    X = np.random.uniform(size=(k, n))
    print(X)
    distances = []
    
    for i in range(k):
        for j in range(i+1, k):
            distance = np.linalg.norm(X[i] - X[j]) / np.sqrt(n)
            distances.append(distance)
    
    return distances

k = 100
n_values = [1, 10, 100, 1000, 10000]

for n in n_values:
    distances = generate_distances(k, n)
    
    plt.hist(distances, bins=20)
    plt.title(f"Histogram dla n={n}")
    plt.xlabel("Odległość / sqrt(n)")
    plt.ylabel("Liczba wystąpień")
    plt.savefig(f'Zad44_hist_n_{n}.png')
    plt.clf()
