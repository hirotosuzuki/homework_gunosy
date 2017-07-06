
#(stop,filter,tfidf,lsi)=(x,o,o,x)


import csv
f =  open("trainingdata.csv",'r')
reader = csv.reader(f)
trainingdata = []
for i in reader:
    trainingdata.append(i)

#trainingdataのカテゴリーラベルを格納
category_trainingdata = [trainingdata[i][0] for i in range(len(trainingdata))]
#trainingdataのテキストデータを格納
text_trainingdata = [trainingdata[i][1:] for i in range(len(trainingdata))]




#リストから特定のワードを除去
def cleaning_list(list,word):
    list_remove = []
    for i in range(len(list)):
        if list[i] == word:
            continue
        else:
            list_remove.append(list[i])

    return list_remove

#テキストデータから特定の複数ワードを除去
def text_cleaning_words(textdata,stop_dictionary):
    cleaned_text_trainingdata = []

    for i in range(len(textdata)):
        x=[]
        x = textdata[i]
        for j in range(len(stop_dictionary)):
            x=cleaning_list(x,stop_dictionary[j])
        cleaned_text_trainingdata.append(x)

    return cleaned_text_trainingdata

'''
#クリーニング１；ストップワードの除去

stop_dictionary = []

text_trainingdata = text_cleaning_words(text_trainingdata,stop_dictionary)
'''


#gensimを使って文書ベクトルを作る
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import gensim
from gensim import corpora
from gensim import matutils
from gensim import models

all_documents = text_trainingdata

dictionary=corpora.Dictionary(all_documents)
#['番組', 'ブラ', 'タモリ', '紹介', '中']...)





#クリーニング２
no_below = 2
no_above = 0.3
dictionary.filter_extremes(no_below=no_below ,no_above= no_above)

dictionary.token2id
#{'番組': 0,'ブラ': 1,'タモリ': 2,'紹介': 3,'中': 4,'さん': 5,
#のように(単語、単語のid)のタプル
#all_documentsの各要素についてbowオブジェクト化する

bow_corpus = [dictionary.doc2bow(d) for d in all_documents]
#[[(0, 5),(1, 2),(2, 3),(3, 3),のように(単語id,出現回数)となっている


#tfidf化
from gensim import models
tfidf_model = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf_model[bow_corpus]

'''
#LSIを用いて各記事の次元をnum_topics次元まで圧縮
num_topics = 100
lsi_model = models.LsiModel(corpus = corpus_tfidf,id2word = dictionary, num_topics = num_topics)

corpus_lsi = lsi_model[corpus_tfidf]
'''

#bowオブジェクトの各要素を頻度の特徴ベクトルにする
#各列のベクトルの要素数はnum_termsで指定
num_terms = len(dictionary)
dense_vector=[matutils.corpus2dense([i],num_terms = num_terms).T[0] for i in corpus_tfidf]


data = dense_vector
target = category_trainingdata


from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(max_depth = 7,

                            n_estimators = 500,
                            bootstrap = 'True',
                           criterion = 'gini')
from sklearn.svm import SVC
svm = SVC(C = 0.9,kernel = 'linear')

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(penalty = 'l2',C = 2)

from sklearn.linear_model import Perceptron
ppn = Perceptron(eta0 = 0.001,
                    n_iter = 10,
                    penalty = 'None')

from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB(alpha = 0.1)

from sklearn.ensemble import VotingClassifier
eclf = VotingClassifier(estimators=[('rf',rf),('svm',svm), ('lr', lr), ('ppn', ppn),('mnb',mnb)], voting='hard')

eclf2 = VotingClassifier(estimators=[('rf',rf),('svm',svm), ('lr', lr), ('ppn', ppn),('mnb',mnb),('eclf',eclf)], voting='hard')


eclf2.fit(data,target)

import pickle
with open('eclf2.pickle',mode = 'wb')as f:
    pickle.dump(eclf2,f)
    f.close()

with open('dictionary.pickle',mode = 'wb') as f:
    pickle.dump(dictionary,f)
    f.close()

with open('tfidf_model.pickle',mode = 'wb') as f:
    pickle.dump(tfidf_model,f)
    f.close()
