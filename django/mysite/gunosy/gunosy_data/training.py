#training.py 学習用ソースコード

import math
import sys
from collections import defaultdict

from pandas import Series,DataFrame
import pandas as pd
xls_file=pd.ExcelFile('trainingdata.xlsx')
trainingdata = xls_file.parse('Sheet2')

import urllib.request
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer


#URLを渡すとグノシー記事本文から名詞のみ抽出される

def url_to_sepatext(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    x=soup.findAll('div',{ "class" : "article gtm-click" })[0].findAll('p')
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


categories = set()     # カテゴリの集合
vocabularies = set()   # ボキャブラリの集合
wordcount = {}         # wordcount[cat][word] あるカテゴリでの、ある単語の出現回数
catcount = {}          # catcount[cat] カテゴリの出現回数
denominator = {}       # denominator[cat] P(word|cat)の分母の値




for i in range(len(trainingdata)):
         #dataのｄ番目の要素もlistで、その０番目（つまりカテゴリー名）
        categories.add(trainingdata.values[i][0]) #setのcategoriesに重複なくカテゴリーを追加

for cat in categories: #カテゴリーの種類分ループ
        wordcount[cat] = defaultdict(int)
        catcount[cat] = 0 #カテゴリーの種類分の大きさのcatcount辞書を作る


for i in range(len(trainingdata)):
    cat=trainingdata.values[i][0]
    doc=url_to_sepatext(trainingdata.values[i][1])
    catcount[cat] += 1
    for word in doc: #d番目の要素のテキスト内の単語の数だけループする
        vocabularies.add(word) #ボキャブラリのset集合に重複なく単語を格納
        wordcount[cat][word] += 1 #d番目の要素の、あるカテゴリーとテキスト内のあるwordが出てくるたびに、wordcount辞書に１足す


# 単語の条件付き確率の分母の値をあらかじめ一括計算しておく（高速化のため）
for cat in categories:
        denominator[cat] = sum(wordcount[cat].values()) + len(vocabularies)
        #あるカテゴリーcatに出てくる全単語数＋重複を除いた総単語数（ゼロ頻度を考慮した時の分母）



import pickle
with open('vocabularies.pickle', mode='wb') as f:
    pickle.dump(vocabularies, f)
    f.close()

with open('categories.pickle', mode='wb') as f:
    pickle.dump(categories, f)
    f.close()

with open('wordcount.pickle', mode='wb') as f:
    pickle.dump(wordcount, f)
    f.close()

with open('catcount.pickle', mode='wb') as f:
    pickle.dump(catcount, f)
    f.close()

with open('denominator.pickle', mode='wb') as f:
    pickle.dump(denominator, f)
    f.close()
