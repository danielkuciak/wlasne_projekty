from bs4 import BeautifulSoup
from collections import Counter
import requests
import spacy
import itertools
import pandas as pd
import matplotlib.pyplot as plt

#pobranie zawartosci pliku z wyrazami niepotrzebnymi, tj. (a,o,i,oraz,lub,w,przez... itp)
with open('test.txt', 'r', encoding='utf-8') as stops:
    stops = list(map(lambda stop: stop.rstrip('\n'), stops))
    stops.extend([',','.','!','-','?',':','[',']','"','\n','—', '…',';','none'])

#przypisanie modelu jezyka polskiego do zmiannej nlp
nlp = spacy.load('pl_core_news_sm')

#zaladowanie zawartoścci z strony
url = "https://wolnelektury.pl/katalog/lektura/antygona.html"
result = requests.get(url)

#wykonanie pieknej zupy z danych ze strony
doc = BeautifulSoup(result.text,'html.parser')

#odnalezenie interesujacych nas kwestii
tekst = doc.find_all('div', class_='verse')

#zamiana kwestii na slowa, nastepnie sprowadzenie slow to wersji podstawowej
#oraz sprawdzenie czy wystepuje w stops-liscie
slowa =[]
for i in range(len(tekst)):
    kwestia = nlp(str(tekst[i].string))
    for token in kwestia:
        token = str(token.lemma_).lower()
        if token not in stops:
            slowa.append(token)

#zliczanie słow
czestotliwosc_slow = Counter(slowa)

#sortowanie danych i wybor 20 najczestnych slow
posortowana = dict(sorted(czestotliwosc_slow.items(), key=lambda x:x[1],reverse=True))
naj20 = dict(itertools.islice(posortowana.items(),20))

#tworzenie tabeli z danych
tabela = pd.DataFrame.from_dict(naj20, orient='index').reset_index()
tabela = tabela.rename(columns={'index':'słowo', 0:'licznik'})

#tworzenie wykresu
tabela.plot(kind='bar', x='slowo' ,y='licznik',title= 'Czestotliwość wystepowanie slow w Antygonie')
plt.show()
