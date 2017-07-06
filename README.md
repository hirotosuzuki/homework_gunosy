# homework
## 概要
gensimとsklearnを用いて文書分類を行った。データ数は増やさなくてもよい、ということだったので前回のデータ320個のままで分類器を学習させた

## アプリケーションの説明



### ディレクトリの構造
* homework_gunosy
  * django
  * requirements.txt
    * mysite
      * gunosy
        * gunosy_data
          * test.py
          * training.py
          * testdata.csv
          * trainingdata.csv
          * 種々のpickleファイル
        * estimator.py
        * views.py
        * urls.py
      * mysite
        * settings.py
        * urls.py
      * templates
        * base.html
        * get_url.html

### ファイルの説明
* trainingdata.csv:教師データ
* testdata.csv:テストデータ
* training.py：学習用ソースコード。trainingdata.csvを用いてアンサンブル分類器eclf2を学習させる。またeclf2とdictionaryとtfidf_modelをpickleファイルに保存する。
* estimator.py:webフォームから入力されたURLをeclf2により文書分類する。
* test.py:testdata.csvを用いて分類器の精度を検証する。

### 処理の流れ
  1. グノシー記事の本文を取得し、０番目にカテゴリー名、１番目以降に名詞の列を格納したリストにする
  2. このリストのテキスト部分から辞書を作成し、クリーニング、tfidf化、LSIによる次元圧縮などの処理を施して、ベクトル化する
  3. このベクトルを分類器に学習させる

## セットアップの方法
#### 環境



* Django 1.11.1
* Python 3.6.0 (Anaconda custom(64bit))
* Pythonモジュール
  * BeautifulSoup4(bs4)
  * urllib
  * Janome
* 形態素解析ツール：gensim  


エラーの出てしまう件ですが、  
ModuleNotFoundError:No module named 'bs4'  
bs4、つまりBeautifulSoup4がインストールできていないと思われます。

requirements.txtにpip freeze で出力されたものを全て記述したので、おそらくエラーは出ないと思います。




#### 手順
* pip install -r requirements.txt
* レポジトリをクローンする。
* コマンドプロンプトやターミナルでhomework_gunosy\django\mysiteに移動
* homework_gunosy\django\mysite\manage.pyを実行
(python manage.py runserver)
* http://127.0.0.1:8000/gunosy/get/　にアクセス
* 記事のURLを入力（例えば　https://gunosy.com/articles/aYAZ2）し、送信ボタンを押すとカテゴリが出力される


## 精度向上のための工夫
1.データの整形という観点から  
  1. クリーニング  

  単語辞書から出現回数がno_below回以下の単語と、no_above％以上の文書に出現する単語を除外  
  dictionary.filter_extremes(no_below,no_above)  

  2. tfidfによる重みづけの変更  

  3. LSI(latent semantic indexing)による次元削減  

  の3点を試した。　

2.分類器という観点から
  1.  複数の分類手法で実験
      1. ロジスティック回帰(LR)
      1. サポートベクトルマシン(SVM)
      1. ランダムフォレスト(RF)
      1. パーセプトロン(ppn)
      1. ガウシアンベイズ分類器(GNB)
      1. 多項式ベイズ分類器(MNB)
  2. 複数の分類器を組み合わせ、多数決方式でカテゴリー判定するアンサンブル学習  
  の２点を試した。


## 分類器の精度
### データ整形と学習機との相性
データ整形の工夫3つをどのように組み合わせると正解率が最も高くなるかを上記の６種類の分類器を用いて検証した。  
各カテゴリー４０個の計320個のデータを用いて、５分割交差検証をグリッドサーチを交えて２回行い、ベストスコアの平均を取った時の正解率を以下の表に示す。

|            	| LR   	| SVM  	| RF   	| ppn  	| GNB  	| MNB    	|
|------------	|------	|------	|------	|------	|------	|--------	|
| xxx        	| 76.8 	| 67   	| 78.5 	| 71.4 	| 71.1 	| 79.6   	|
| oxx        	| 80.2 	| 70.5 	| 76.8 	| 72.7 	| 71.1 	| 80.5   	|
| xox        	| 80.5 	| 81.8 	| 78.6 	| 75.8 	| 66.7 	| 80.5   	|
| xxo(100)   	| 73.3 	| 66.8 	| 63.4 	| 70   	| 31.5 	| エラー 	|
| xxo(200)   	| 74.9 	| 62.3 	| 63   	| 70   	| 34.2 	| エラー 	|
| xxo(300)   	| 77.4 	| 66.7 	| 61.7 	| 70.5 	| 31.6 	| エラー 	|
| xxo(400)   	| 76.8 	| 67   	| 62   	| 71.4 	| 31.6 	| エラー 	|
| xxo(500)   	| 76.8 	| 67   	| 61   	| 71.4 	| 31.6 	| エラー 	|
| oox        	| 81.5 	| 80.5 	| 77.1 	| 81.2 	| 66.7 	| 81.2   	|
| ooo(400)   	| 76.8 	| 80.5 	| 76   	| 80.2 	| 52.6 	| エラー 	|  


* 表の見方  
  * 縦軸がデータ整形の組み合わせである。  
  * 例えば  
ooxは、(クリーニング,tfidfによる重みづけ,LSI)=(あり、あり、なし)  
xxo(300)は、(クリーニング,tfidfによる重みづけ,LSI)=(なし、なし、あり)かつ、LSIで300次元に圧縮した、という意味  
  * 横軸は分類器である。  
  * クリーニングは出現回数が２回未満の単語と、３０％以上の文書に出現する単語を除外した

* 解釈  
  * xxxの時に比べて正解率が上昇していれば、その手法が有効であると判断した。  
  * クリーニングはRF以外すべての分類器で正解率が上昇したので、有効  
  * tfidfによる重みづけはGNB以外の分類器で正解率が上昇したので、有効  
  * LSIによる次元圧縮は、正解率を低下させることが多く、分類器や圧縮する次元によっては低下しない場合もあるが、正解率を上昇させることはほぼなかった。計算時間の短縮が必要な場合には有効かもしれないが、今回320個のデータだけを用いているので、有効ではないと判断した。  


  以上より、クリーニングとtfidfのみを用いてデータを整形することに決めた。


### アンサンブル学習機
* クリーニングあり、tfidfあり、LSIなし、のooxの時に正解率が高いのはガウシアンベイズ分類器以外の分類器であるので、この５つの分類器を組み合わせてアンサンブル分類器を作成した  
* 分類器の組み合わせを様々試した結果  
  まず(RF,SVM,LR,ppn,MNB)の５つを用いて多数決分類器eclfを作り、(RF,SVM,LR,ppn,MNB,eclf)の６つを用いて多数決分類器eclf2を作ると、最もロバストで正解率の高い分類器ができた。
*  (RF,SVM,LR,ppn,MNB,eclf,eclf2)の７つの分類器で、より詳細なグリッドサーチを行い、ベストな分類器で、データ３２０個を用いて５分割交差検証を行った。

  この時の正解率、適合率、再現率、F値は以下のようになった。

|                 | LR   | SVM  | RF   | ppn  | MNB  | eclf |eclf2 |
|-----------------|------|------|------|------|------|------|------|
| accuracy        | 81.2 | 81.5 | 76.4 | 81.2 | 81.1 | 82.1 | 82.4 |
| precision_macro | 82.8 | 84.9 | 77.1 | 82.8 | 80.7 | 84.6 | 83.9 |
| recall_macro    | 81.5 | 81.5 | 75.8 | 81.2 | 81.2 | 82.4 | 82.8 |
| f1_macro        | 81.1 | 81.8 | 74.8 | 80.9 | 80.3 | 82.4 | 82.5 |

* データ３２０個を学習用とテスト用で８：２に分け、clf2を用いて予測した結果をclassification_reportで出力したところ以下のようになった。(一例)

| category  	| precision 	| recall 	| f1-score 	|
|-----------	|-----------	|--------	|----------	|
| エンタメ  	| 100       	| 75     	| 86       	|
| スポーツ  	| 100       	| 83     	| 91       	|
| おもしろ  	| 100       	| 78     	| 88       	|
| 国内      	| 55        	| 86     	| 67       	|
| 海外      	| 86        	| 60     	| 71       	|
| コラム    	| 45        	| 71     	| 56       	|
| IT・科学  	| 67        	| 50     	| 57       	|
| グルメ    	| 78        	| 100    	| 88       	|
| avg/total 	| 82        	| 77     	| 78       	|  





### testdata.csvのデータ８０個の分類  
trainingdata.csvの３２０個のデータを用いてeclf2を学習させ、testdata.csvのデータを分類したところ以下のようになった。


| category  	| precision 	| recall 	| f1-score 	|
|-----------	|-----------	|--------	|----------	|
| エンタメ  	| 100       	| 90     	| 95       	|
| スポーツ  	| 100       	| 80     	| 89       	|
| おもしろ  	| 89        	| 80     	| 84       	|
| 国内      	| 64        	| 90     	| 75       	|
| 海外      	| 90        	| 90     	| 90       	|
| コラム    	| 100       	| 60     	| 75       	|
| IT・科学  	| 75        	| 90     	| 82       	|
| グルメ    	| 83        	| 100    	| 91       	|
| avg/total 	| 88        	| 85     	| 85       	|

  再現率、適合率、F値が平均して８０％を超えており、交差検証の結果とほぼ合致する。  

## 追記
### 精度向上のために試したが失敗したこと  
  1. １単語単位でストップワードを指定できるようにし、「％」や「・」などの直観的に明らかに不要そうな単語を３０単語ほど除去してみたが、正解率の向上には寄与しないだけでなく、むしろ下がってしまう場合もあったため、断念した
  2. 上記の分類器だけでなく、決定木やｋ近傍法でも分類してみたが、ハイパーパラメータをどういじっても精度が向上しないため断念した。  



### さらなる精度向上のために今後試したいこと  
  1. 今回次元圧縮にLSIを用いたが、LDAなど別の方法で圧縮する
  2. DeepLearningを用いてみる
  3. アンサンブル学習において、純粋な多数決にするのではなく、それぞれの分類器に重みづけをする
  4. それぞれの分類器に精度の高いカテゴリー、低いカテゴリーがあるならば、多数決を取るときに、各分類器にカテゴリーごとに重みづけをする。この課題の場合、６つの分類器で8つのカテゴリーであるから６×８の４８個の重みを調整する  
  5. アンサンブル学習において、それぞれの分類器に同じデータで学習させるのではなく、元データからランダムに復元・非復元抽出されたデータで学習させる。
