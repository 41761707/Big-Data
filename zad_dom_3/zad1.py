import sys
import random

def minHash(L, num_hashes,coefficients):
    min_values = [sys.maxsize] * num_hashes

    for x in L:
        for i in range(num_hashes):
            hash_value = my_hash(x,coefficients[i][0],coefficients[i][1],coefficients[i][2],coefficients[i][3])
            #print("{} - {}".format(x,hash_value))
            if hash_value < min_values[i]:
                min_values[i] = hash_value

    return min_values

def rand_prime():
    while True:
        p = random.randrange(2 ** 32, 2 ** 34, 2)
        if all(p % n != 0 for n in range(3, int((p ** 0.5) + 1), 2)):
            return p

def my_hash(x,a,b,p,m):
    return ((a * hash(x) + b) % p) % m

def main():
    num_hashes = int(sys.argv[1])
    coefficients = []
    for i in range(num_hashes):
        a = random.randint(1,1000)
        b = random.randint(1,1000)
        p = rand_prime()
        m = 2 ** 32 - 1
        coefficients.append((a,b,p,m))
    for i in range(num_hashes):
        print("Hash nr {}: (({} * hash(x) + {}) % {}) % {}".format(i,coefficients[i][0],coefficients[i][1],coefficients[i][2],coefficients[i][3]))
    L = ["przykladowe","slowa","do","implementacji","minhash"]
    result = minHash(L, num_hashes,coefficients)
    print(result)

if __name__ == '__main__':
    main()


