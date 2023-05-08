import pandas as pd
import requests
import matplotlib.pyplot as plt

import random

def reservoir_sampling(stream, k):
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir

with open('Bitcoin.csv') as file:
    values = []
    for line in file:
        currentline = line.split(",")
        extracted = currentline[3] +','+ currentline[4]
        extracted = extracted.replace('.','')
        extracted = extracted.replace(',','.')
        extracted = extracted[1:len(extracted)-1]
        values.append(float(extracted))
    sample = reservoir_sampling(values, 40)
    print(len(values))
    print(len(sample))
    print(sample)
    plt.title("Wykres notowań")
    plt.plot(values)
    plt.savefig("Notowania.png")
    plt.clf()
    plt.title("Próbka")
    plt.plot(sample)
    plt.savefig("Probka.png")
    plt.clf()

'''# pobierz notowania z API
url = "https://api.coindesk.com/v1/bpi/historical/close.json?start=2016-05-08&end=2021-05-08"
response = requests.get(url)
data = response.json()

# konwertuj dane do obiektu DataFrame
df = pd.DataFrame(data["bpi"].items(), columns=["date", "price"])
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].astype(float)

# wygeneruj losową próbkę 40 notowań

# wygeneruj wykresy notowań i próbki
plt.plot(df["date"], df["price"], label="Bitcoin")
plt.scatter(df.loc[df["price"].isin(sample)]["date"], sample, c="r", label="Losowa próbka")
plt.legend()
plt.savefig('Vitter.png')
plt.clf()
'''