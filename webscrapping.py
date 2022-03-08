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


class GetWeb:
    '''POBIERANIE STRONY'''
    def __init__(self, url):
        self.url = url

    def webContent(self, attribute, class_):
        result = requests.get(self.url)
        doc = BeautifulSoup(result.text, 'html.parser')
        text = doc.find_all(attribute,class_)
        return text

class AnalysisWeb:
    '''METODY DO ANALIZY STRON'''
    def __init__(self,content):
        self.content = content

    def transformData(self):
        words= []
        for i in range(len(self.content)):
            sentences = nlp(str(self.content[i].string))
            for token in sentences:
                token = str(token.lemma_).lower()
                if token not in stops:
                    words.append(token)
        return words

    def twenty_most_often_words(self):
        frequecy = Counter(self)
        sortedd = dict(sorted(frequecy.items(), key=lambda x: x[1], reverse=True))
        top20 = dict(itertools.islice(sortedd.items(), 20))
        return top20


def showPlot(data,x,y,title):
    table =  pd.DataFrame.from_dict(data, orient='index').reset_index()
    table = table.rename(columns={'index':'word', 0:'counter'})
    table.plot(kind='bar', x= x, y= y, title= title)
    plt.show()

page = GetWeb("https://wolnelektury.pl/katalog/lektura/antygona.html")
text = page.webContent('div', class_='verse')
words = AnalysisWeb(text).transformData()
top20  = AnalysisWeb.twenty_most_often_words(words)
showPlot(top20, x='word' ,y='counter',title= 'A frequency of the occurrence of words in the "Antigone"')
