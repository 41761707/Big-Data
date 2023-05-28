import sys
import re
import random
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import collections

# Robione na kolanie o 5, więc dość nieoptymalne, ale przynajmniej działa

#info z dc:
#Bierzemy dokument i obliczamy wektor min haszy na jego k gramach. Na tych wektorach uruchamiany kmeans  i otrzymujemy klasteryzację dokumentów
#Nie kumam troche co mi to k_means daje, moze trzeba to graficznie potraktowac?
def k_means(arr,filenames,k,num_hashes):
    for file in filenames:
        tmp = np.zeros(num_hashes)
        index_counter = 0
        for word in arr:
            if word[0] == file:
                tmp[index_counter] = word[1]
                index_counter = index_counter + 1

        # Konwertowanie danych do wymaganego formatu
        X = tmp.reshape(-1, 1)
        # Użycie algorytmu k-means do klasteryzacji
        k = 7  # Liczba klastrów
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        # Wyświetlanie przypisanych klastrów
        counts = collections.Counter(kmeans.labels_)
        print(file.split("/")[-1], ': ',counts)
        '''for i, num in enumerate(X):
            cluster_label = kmeans.labels_[i]
            print(f"Liczba {num} należy do klastra {cluster_label}")'''


# Funkcja generująca losową dużą liczbę pierwszą
def rand_prime():
    while True:
        p = random.randrange(2 ** 32, 2 ** 34, 2)
        if all(p % n != 0 for n in range(3, int((p ** 0.5) + 1), 2)):
            return p

# Funkcja generująca dobrą rodzinę haszującą
# https://en.wikipedia.org/wiki/Universal_hashing#Hashing_integers
# robię hash(x) zamiast x żeby dostać liczbę
# a można tak zrobić, bo wiadomo że
# dla wszystkich x1,x2 ze zbioru słów takich, że x1=x2 mamy hash(x1) = hash(x2)
def my_hash(x,a,b,p,m):
    return ((a * hash(x) + b) % p) % m

#Porówanie styli 
#x - zbior słów
#k - ile słów rozpatrujemy (k-gram) [x_i,...,x_i+k-1] <- wycinek zbioru x
#a,b,p,m - stałe do my_hash
def style_comparison(x,k,a,b,p,m):
    min_value = sys.maxsize
    for i in range(0,len(x)-k+1):
        for j in range(i,i+k):
            value = my_hash(x[j],a,b,p,m)
            if value < min_value:
                min_value = value
    return min_value
            
# Czytanie z pliku
# Oczyszczanie inputu ze spacji, dziwnych znaków, jak masz len(x) < 3 to wyrzucamy
# I jak juz trafilismy to slowo to też wyrzucamy (nie wiem czy tak powinno być w sumie,
# ale te prawdopodobieństwa Jaccard'a itd. działają na zbiorach
# więc taka jest pierwsza intuicja, w razie czego do poprawy)
def read_from_file(filename):
    words = []
    f = open(filename)
    for word in f.read().split():
        if(len(word)) < 3:
            continue
        word = word.lower()
        word = re.sub(r'[^a-z0-9]+', '', word)
        if(len(word)) <3:
            continue
        if word in words:
            continue
        words.append(word)
    return words

# Wszystko w mainie bo czemu by nie 
# k - jak długi wycinek zbioru rozpatrumey 
# num_hashes - ile hashy rozpatrujemy
# path - gdzie są pliki (folder)
def main():
    k = int(sys.argv[1]) #>= 1
    num_hashes = int(sys.argv[2])
    path = sys.argv[3] #/home/radikey/studia/Magisterka/Semestr1/Big-Data/zad_dom_3/chapters/chapters/
    # Generujemy współczynniki do my_hash
    coefficients = []
    for i in range(num_hashes):
        a = random.randint(1,1000)
        b = random.randint(1,1000)
        p = rand_prime()
        m = 2 ** 32 - 1
        coefficients.append((a,b,p,m))
    #for i in range(num_hashes):
        #print("Hash nr {}: (({} * hash(x) + {}) % {}) % {}".format(i,coefficients[i][0],coefficients[i][1],coefficients[i][2],coefficients[i][3]))
    #filenames = ["/home/radikey/studia/Magisterka/Semestr1/Big-Data/zad_dom_3/chapters/chapters/hamlet_chapter1.txt","/home/radikey/studia/Magisterka/Semestr1/Big-Data/zad_dom_3/chapters/chapters/romeoJuliet_chapter1.txt"]
    # Wczytujemy pliki z folderu

    filenames = []
    for filename in os.listdir(path):
        filenames.append(path + filename)
    #print(filenames)
    min_values_per_file = []
    words = []
    # Pobieramy słowa z każdego pliku do words
    for filename in filenames:
        words.append(read_from_file(filename))

    # Pobieramy minimalną wartośc dla każdego pliku i dla każdego hasha
    for i in range(len(filenames)):
        for j in range(num_hashes):
            min_values_per_file.append((filenames[i],(style_comparison(words[i],k,coefficients[j][0],coefficients[j][1],coefficients[j][2],coefficients[j][3]))))
    #print(min_values_per_file)

    jaccard_exp = []
    jaccard_true = []

    #jaccard_exp
    # Jedziemy po wszystkich wartosciach z min_values_per_file
    # Z racji tego, że jest to krotka (nazwa_pliku, wartość dla hasza) 
    # to sobie sprawdzamy, czy aktualny plik to ten z krotki 
    # i do tmp wrzucamy wartość dla hasza
    for i in range(len(filenames)):
        for j in range(i+1,len(filenames)):
            tmp_1 = []
            tmp_2 = []
            for value in min_values_per_file:
                if value[0] == filenames[i]:
                    tmp_1.append(value[1])
                if value[0] == filenames[j]:
                    tmp_2.append(value[1])
            #print(tmp_1)
            #print(tmp_2)

            jaccard_exp.append([filenames[i],filenames[j],len(list(set(tmp_1).intersection(tmp_2)))/len(tmp_1)])
    #print("JACCARD_EXP: ",jaccard_exp)

    #jaccard_true
    # To było na wykładzie to nie ma co tłumaczyć
    # |A n B| / |A u B| - koniec zabawy

    for i in range(len(filenames)):
        for j in range(i+1,len(filenames)):
            intersections = len(list(set(words[i]).intersection(words[j])))
            unions = (len(words[i]) + len(words[j])) - intersections
            jaccard_true.append([filenames[i],filenames[j],intersections/unions])
    #print("JACCARD_TRUE: ",jaccard_true)

    #Porownanie wartosci
    for i in range(len(jaccard_exp)):
        print("{} - {} : EXP: {}, TRUE: {}, DIFF: {}".format(jaccard_exp[i][0].split("/")[-1],
                                                            jaccard_exp[i][1].split("/")[-1],
                                                            jaccard_exp[i][2],
                                                            jaccard_true[i][2],
                                                            abs(jaccard_true[i][2]-jaccard_exp[i][2])))
        
    #k-means
    k_means(min_values_per_file,filenames,k,num_hashes)
            
if __name__ == '__main__':
    main()