import html2text
import requests
import queue
import re
import nltk
import json
from collections import Counter
from bs4 import BeautifulSoup
from google import search
from stop_words import get_stop_words
from stemming.porter2 import stem
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from heapq import *
from multiprocessing import Pool
#lemma = nltk.corpus.wordnet.WordNetLemmatizer()

non_word_list = ['[',']','*', '(',')','\\','/','&']
word_count = []
lemma = WordNetLemmatizer()
stop = stopwords.words('english')

def get_phrase():
    phrase =  str(input("Input phrase to search articles for: "))

    return phrase


def soupify(url):
    soup = BeautifulSoup(url.text,"html.parser")
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
    return text

def get_count(texts):
    for text in texts:
        for word in text.split():
            word = word.lower()
            if word not in stop:
                #if word not in stop_words2:
                    #if word not in stop:

                if word not in non_word_list:
                    if not word.isdigit():
                        stemword = lemma.lemmatize(word)
                        #stemword = stem(stemword)
                        word_count.append(stemword)

    cnt = Counter(word_count)
    queue2 = []
    #print(cnt)

    not_done = len(queue2)

    return cnt.most_common()[:6]

def get_key_words(phrase, gen_sums=None):
    url_list = []
    #f = open('something.html','w')
    urls = []
    if gen_sums == None:

        for x in search(phrase, stop = 1):
            #url_list += [x]
            urls += [requests.get(x)]

        #f.write(urls.text)
        #f.close()
        pool = Pool(len(urls))
        texts = pool.map(soupify,urls)
        for text in texts:
            for word in text.split():
                word = word.lower()
                if word not in stop:
                    #if word not in stop_words2:
                        #if word not in stop:

                    if word not in non_word_list:
                        if not word.isdigit():
                            stemword = lemma.lemmatize(word)
                            #stemword = stem(stemword)
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

        not_done = len(queue2)

        return cnt.most_common()[:6]

    else: #done filtering
        for x in search(phrase, stop = 1):
            url_list += [x]
        return url_list

def main():

    phrase = get_phrase()
    top_5 = get_key_words(phrase)
    resulting_words = []
    for i in top_5:
        resulting_words += [i[0] + ' ']

    #(resulting_words)
    new_phrase = ''.join(resulting_words)
    print("new phrase to search with ",new_phrase)
    urls = get_key_words(new_phrase, gen_sums = 1)

    p = Pool (len(urls))
    p.map(get_summary,urls)
def get_summary(url):
    api_key = open('api_key.txt','r').readline().strip()


    params = {"url": url, "apikey":api_key}
    r = requests.get("https://api.havenondemand.com/1/api/sync/extractconcepts/v1", params = params)
    sum_list = []
    if r.status_code == 200:
        list2 = r.json()['concepts']
        for dic in list2:
            sum_list += [dic['concept'] + ' ']
        summary = ''.join(sum_list)
        print(summary)

if __name__ == '__main__':
    main()
