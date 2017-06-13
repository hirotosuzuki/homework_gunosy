
#new test.py
from naivebayes import *


#テストデータを読み込んで、trainingdataに格納
import csv

f =  open("testdata.csv",'r')
reader = csv.reader(f)
trainingdata = []
for i in reader:
    trainingdata.append(i)


category_dict = {1:"エンタメ",2:"スポーツ",3:"おもしろ",4:"国内",5:"海外",6:"コラム",7:"IT・科学",8:"グルメ"}
category_dict_inv={v:k for k, v in category_dict.items()}


real_number = [] #真のカテゴリー（1～8）
judge_number =[] #判定結果のカテゴリー（1～8）

Accuracy = 0 #正解率
point = 0
for i in range(len(trainingdata)):
    test=trainingdata[i][1:] #trainingdataのi行目の２番目以降、つまり単語の列
    try:
        test=trainingdata[i][1:]
        classify(test)
        if classify(test)==category_dict[int(trainingdata[i][0])]:
            point +=1
    except :
        print(i)
        continue

    real_number.append(int(trainingdata[i][0])) #trainingdataのi行目の１番、つまり真のカテゴリー
    judge_number.append(category_dict_inv[classify(test)])
Accuracy = point/len(trainingdata)*100


# ０行目が真の値、１行目が判定結果
#y = [[1,1,2,2,3,2],[1,2,2,3,2,1]]

m = len(real_number) # データの個数

# tp+fnの和
tp_fn = [0 for i in range(8)]
# tp+fpの和
tp_fp = [0 for i in range(8)]
tp=[0 for i in range(8)]

for j in range(1,9):
    for i in range(m):

        if category_dict[real_number[i]] == category_dict[j]  :
            tp_fn[j-1] +=1

        if category_dict[judge_number[i]] == category_dict[j]  :
            tp_fp[j-1] +=1

        if category_dict[real_number[i]] == category_dict[j] and category_dict[judge_number[i]] == category_dict[j]:
            tp[j-1] += 1


Precision= [0 for i in range(8)] #適合率
Recall = [0 for i in range(8)]   #再現率

import math

for i in range(8):
    #分母が０の時の例外処理
    if tp_fp[i]==0:
        Precision[i] = None
    if tp_fn[i]==0:
        Recall[i] = None

    else:

        Precision[i] = round(tp[i]/tp_fp[i],3)
        Recall[i]   = round(tp[i]/tp_fn[i],3)
F_measure = []

for i in range(len(Recall)):
    if Precision[i] == None or Recall[i] == None:
        pass
    else:
        x = 2*Precision[i]*Recall[i]/(Precision[i]+Recall[i])
        F_measure.append(round(x,3))

print("正解率"+str(Accuracy)+"％\n")

for i in range(1,9):
    print("カテゴリー:「"+category_dict[i]+"」の\n")
    print("適合率："+str(Precision[i-1]*100)+"％\n")
    print("再現率："+str(Recall[i-1]*100)+"％\n")
    print("F値："+str(F_measure[i-1]*100)+"％\n")
