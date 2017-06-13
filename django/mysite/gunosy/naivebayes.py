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


def wordProb(word, cat):#そのカテゴリーの中でこの単語はどれくらいの確率ででるか、みたいな
        """単語の条件付き確率 P(word|cat) を求める"""
        # ラプラススムージングを適用
        # wordcount[cat]はdefaultdict(int)なのでカテゴリに存在しなかった単語はデフォルトの0を返す
        # 分母はtrain()の最後で一括計算済み
        return float(wordcount[cat][word] + 1) / float(denominator[cat])
        #あるカテゴリーの中のある単語の出現回数÷そのカテゴリーの分母


def score(doc, cat):
        """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
        total = sum(catcount.values())  # 総文書数
        #catcount={'no': 1, 'yes': 3},catcount.values()=dict_values([1, 3])

        score = math.log(float(catcount[cat]) / total)  # log P(cat)
        #あるカテゴリーの、総文書数に占める割合

        for word in doc:
            # logをとるとかけ算は足し算になる
            score += math.log(wordProb(word, cat))  # log P(word|cat)
            #P(cat|doc)=P(doc|cat)*P(cat)
            #          =P(word1|cat)*P(word2|cat)...*P(cat)
            #これのlogを取ると、上式のようになる

        return score


def classify(doc):
        """事後確率の対数 log(P(cat|doc)) がもっとも大きなカテゴリを返す"""
        best = None
        max = -1000000000
        for cat in catcount.keys(): #catcount.keys()=dict_keys(['no', 'yes'])
            #カテゴリーの種類分だけループ
            p = score(doc, cat) #log(P(cat|doc))
            if p > max:
                max = p
                best = cat
        return category_dict[int(best)]


import pickle
with open('./gunosy/gunosy_data/vocabularies.pickle', mode='rb') as f:
    vocabularies= pickle.load(f)

with open('./gunosy/gunosy_data/categories.pickle', mode='rb') as f:
        categories= pickle.load(f)

with open('./gunosy/gunosy_data/wordcount.pickle', mode='rb') as f:
    wordcount= pickle.load(f)


with open('./gunosy/gunosy_data/catcount.pickle', mode='rb') as f:
    catcount= pickle.load(f)


with open('./gunosy/gunosy_data/denominator.pickle', mode='rb') as f:
        denominator=pickle.load(f)
