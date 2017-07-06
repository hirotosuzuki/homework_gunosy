import math
import sys
from collections import defaultdict
import urllib.request
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer

category_dict = {1:"エンタメ",2:"スポーツ",3:"おもしろ",4:"国内",5:"海外",6:"コラム",7:"IT・科学",8:"グルメ"}

def url_to_sepatext(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')


    try:
        x=soup.findAll('div',{ "class" : "article gtm-click" })[0].findAll('p')

    except:
        x=soup.findAll('div',{"class":"article"})[0].findAll('p')



    y=str()
    for i in range(len(x)):
        y += x[i].get_text()

    t = Tokenizer()

    # ユニコード文字列を渡す必要がある
    tokens = t.tokenize(y)

    #形態素解析で名詞を抽出
    a = []
    for token in tokens:
        if '名詞' in token.part_of_speech:
            a.append(token.base_form)

    #アスタリスクを削除したリストにする
    for i in range(len(a)):
        a[i] = a[i].strip('*')

    while(True):
        try:
            a.remove('')
        except ValueError:
            break

    return a

#urlが渡されたら、判定を返す


import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import gensim
from gensim import corpora
from gensim import matutils
from gensim import models

import pickle

with open('./gunosy/gunosy_data/eclf2.pickle', mode='rb') as f:
    eclf2= pickle.load(f)

with open('./gunosy/gunosy_data/tfidf_model.pickle', mode='rb') as f:
    tfidf_model= pickle.load(f)

with open('./gunosy/gunosy_data/dictionary.pickle', mode='rb') as f:
    dictionary= pickle.load(f)




def classify(text):
    category_dict = {1:"エンタメ",2:"スポーツ",3:"おもしろ",4:"国内",5:"海外",6:"コラム",7:"IT・科学",8:"グルメ"}

    text_list =[]
    text_list.append(text)
    test_bow_corpus = [dictionary.doc2bow(i) for i in text_list]
    test_corpus_tfidf= tfidf_model[test_bow_corpus]
    x_test_vector = [matutils.corpus2dense([i],
                                           num_terms = len(dictionary)).T[0] for i in test_corpus_tfidf]

    y_pred = eclf2.predict(x_test_vector)[0]
    return category_dict[int(y_pred)]
