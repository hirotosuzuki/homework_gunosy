import csv
f =  open("testdata.csv",'r')
reader = csv.reader(f)
testdata = []
for i in reader:
    testdata.append(i)

#trainingdataのカテゴリーラベルを格納
category_testdata = [testdata[i][0] for i in range(len(testdata))]
#trainingdataのテキストデータを格納
text_testdata = [testdata[i][1:] for i in range(len(testdata))]


import pickle

with open('eclf2.pickle', mode='rb') as f:
    eclf2= pickle.load(f)

with open('tfidf_model.pickle', mode='rb') as f:
    tfidf_model= pickle.load(f)

with open('dictionary.pickle', mode='rb') as f:
    dictionary= pickle.load(f)


import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import gensim
from gensim import corpora
from gensim import matutils
from gensim import models

test_bow_corpus =  [dictionary.doc2bow(i) for i in text_testdata]

test_corpus_tfidf =tfidf_model[test_bow_corpus]



x_test_vector = [matutils.corpus2dense([i],num_terms = len(dictionary)) .T[0] for i in test_corpus_tfidf]





y_pred = eclf2.predict(x_test_vector)


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
print(classification_report(category_testdata,y_pred,target_names = ['エンタメ', 'スポーツ', 'おもしろ','国内','海外','コラム','IT・科学','グルメ']))
