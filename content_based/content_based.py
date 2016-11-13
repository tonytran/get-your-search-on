import html2text
import requests
import queue
import re
import nltk
from collections import Counter
from bs4 import BeautifulSoup
from google import search
from stop_words import get_stop_words
from stemming.porter2 import stem
from nltk.corpus import stopwords
from heapq import *
#lemma = nltk.corpus.wordnet.WordNetLemmatizer()
stop_words = get_stop_words('english')
non_word_list = ['[',']','*', '(',')','\\','/']
word_count = []
stop_words2 = []
f = open('stop_words.txt', 'r')
stop = stopwords.words('english')
for word in f:
    stop_words2.append(word)
    stop_words2.append(word.upper())
f.close()
def get_phrase():
    phrase =  str(input("Input phrase to search articles for: "))

    return phrase

def main():
    encountered_list = []

    phrase = get_phrase()
    url_list = []
    #f = open('something.html','w')

    for x in search(phrase, stop = 1):
        #url_list += [x]
        urls = requests.get(x)

    #f.write(urls.text)
    #f.close()

        soup = BeautifulSoup(urls.text,"html.parser")
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        for word in text.split():
            word = word.lower()
            if word not in stop:
                #if word not in stop_words2:
                    #if word not in stop:

                if word not in non_word_list:
                    if not word.isdigit():
                        stemword = stem(word)
                        word_count.append(stemword)

                        #else:
                            #word_count[stemword] += 1


        #for key in word_count:
            #print(key, ': ',word_count[key])
    #filtered_word_list = word_count[:] #make a copy of the word_list
    #filtered_words = [word for word in word_count if word not in stopwords.words('english')]


    cnt = Counter(word_count)
    queue2 = []
    #print(cnt)
    print(type(cnt.most_common()))

    not_done = len(queue2)

    for i in cnt.most_common()[:6]:

main()
