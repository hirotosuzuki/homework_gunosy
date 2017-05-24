#テスト用コード

xls_file=pd.ExcelFile('testdata.xlsx')
testdata = xls_file.parse('Sheet1')
category_dict = {1:"エンタメ",2:"スポーツ",3:"おもしろ",4:"国内",5:"海外",6:"コラム",7:"IT・科学",8:"グルメ"}


#カテゴライズの正答率を求める

point=0

for i in range(len(testdata)):
    test=url_to_sepatext(testdata.values[i][1])
    classify(test)
    if classify(test)==category_dict[testdata.values[i][0]]:
        point +=1

ratecorrect = point/len(testdata)*100
ratecorrect
