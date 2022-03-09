from bs4 import BeautifulSoup
from collections import Counter
import requests
import spacy
import itertools
import pandas as pd
import matplotlib.pyplot as plt

class GetWeb:
    def __init__(self, url):
        self.url = url

    def webContent(self, attribute, class_):
        result = requests.get(self.url)
        doc = BeautifulSoup(result.text, 'html.parser')
        text = doc.find_all(attribute,class_)
        
        return text

class AnalysisWeb:
    def __init__(self,content):
        self.content = content

    def transformData(self, file, kind, encoding):
        with open(file, kind ,encoding= encoding) as stops:
            stops = list(map(lambda stop: stop.rstrip('\n'), stops))
            stops.extend([',', '.', '!', '-', '?', ':', '[', ']', '"', '\n', '—', '…', ';', 'none'])

        nlp = spacy.load('pl_core_news_sm')

        words = []
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

if __name__ == "__main__":
    page = GetWeb("https://wolnelektury.pl/katalog/lektura/antygona.html")
    text = page.webContent('div', class_='verse')
    words = AnalysisWeb(text).transformData(file = 'stops.txt', kind = 'r', encoding = 'utf-8')
    top20 = AnalysisWeb.twenty_most_often_words(words)
    
    showPlot(top20, x='word' ,y='counter',title= 'A frequency of the occurrence of words in the "Antigone"')
