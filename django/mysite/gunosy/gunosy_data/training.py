
# coding: utf-8

# In[1]:

#new training.py 学習用ソースコード

import math
import sys
from collections import defaultdict


categories = set()     # カテゴリの集合
vocabularies = set()   # ボキャブラリの集合
wordcount = {}         # wordcount[cat][word] あるカテゴリでの、ある単語の出現回数
catcount = {}          # catcount[cat] カテゴリの出現回数
denominator = {}       # denominator[cat] P(word|cat)の分母の値

import csv 

f =  open("trainingdata.csv",'r')
reader = csv.reader(f)
trainingdata = []
for i in reader:
    trainingdata.append(i)


for i in range(len(trainingdata)):
         #dataのｄ番目の要素もlistで、その０番目（つまりカテゴリー名）
        categories.add(trainingdata[i][0]) #setのcategoriesに重複なくカテゴリーを追加

for cat in categories: #カテゴリーの種類分ループ
        wordcount[cat] = defaultdict(int)
        catcount[cat] = 0 #カテゴリーの種類分の大きさのcatcount辞書を作る
        

for i in range(len(trainingdata)):
    cat=trainingdata[i][0]
    doc=trainingdata[i][1:]
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


# In[3]:

categories


# In[4]:

vocabularies


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



