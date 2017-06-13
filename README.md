# homework
## アプリケーションの説明



### ディレクトリの構造
* homework_gunosy  
  * django  
    * mysite  
      * gunosy
        * gunosy_data
          * test.py
          * training.py
          * testdata.csv
          * trainingdata.csv
          * 種々のpickleファイル
        * naivebayes.py
        * views.py
        * urls.py
      * mysite
        * settings.py
        * urls.py       
      * templates
        * base.html
        * get_url.html  

### 細かい解説
* trainingdata.csv:教師データ
* testdata.csv:テストデータ
* training.py：学習用ソースコード。trainingdata.csvを用いて事後確率などを求め、それを種々のpickleファイルに保存する。
* naivebayes.py:webフォームから入力されたURLをナイーブベイズにより文書分類する。
* test.py:testdata.csvを用いて分類器の精度を検証する。


## セットアップの方法
#### 環境
* Django 1.11.1
* Python 3.6.0 (Anaconda 4.3.1(64bit))
* Pythonモジュール
  * BeautifulSoup4
  * urllib
  * Janome

#### 手順
* レポジトリをクローンする。
* コマンドプロンプトやターミナルでhomework_gunosy\django\mysiteに移動
* homework_gunosy\django\mysite\manage.pyを実行  
(python manage.py runserver)
* http://127.0.0.1:8000/gunosy/get/　にアクセス  
* 記事のURLを入力（例えば　https://gunosy.com/articles/aYAZ2）し、送信ボタンを押すとカテゴリが出力される




## 分類器の精度
gunosy_dataフォルダ内のtestdata.csvを精度測定用のテストデータとして用いる。  
指標として正解率、適合率、再現率、F値を用いた。

### 教師データを各カテゴリーごとに40個の、計320個用いたとき  
#### テストデータを各カテゴリーごとに5個の、計40個用いると,

正解率90.0％  
カテゴリー:「エンタメ」の

適合率：100.0％

再現率：80.0％

F値：88.9％

カテゴリー:「スポーツ」の

適合率：100.0％

再現率：80.0％

F値：88.9％

カテゴリー:「おもしろ」の

適合率：100.0％

再現率：80.0％

F値：88.9％

カテゴリー:「国内」の

適合率：100.0％

再現率：100.0％

F値：100.0％

カテゴリー:「海外」の

適合率：83.3％

再現率：100.0％

F値：90.9％

カテゴリー:「コラム」の

適合率：100.0％

再現率：80.0％

F値：88.9％

カテゴリー:「IT・科学」の

適合率：62.5％

再現率：100.0％

F値：76.9％

カテゴリー:「グルメ」の

適合率：100.0％

再現率：100.0％

F値：100.0％  

#### テストデータを各カテゴリーごとに10個の、計80個用いると、  

正解率83.75％

カテゴリー:「エンタメ」の

適合率：100.0％

再現率：90.0％

F値：94.7％

カテゴリー:「スポーツ」の

適合率：100.0％

再現率：90.0％

F値：94.7％

カテゴリー:「おもしろ」の

適合率：85.7％

再現率：60.0％

F値：70.6％

カテゴリー:「国内」の

適合率：75.0％

再現率：90.0％

F値：81.8％

カテゴリー:「海外」の

適合率：76.9％

再現率：100.0％

F値：86.9％

カテゴリー:「コラム」の

適合率：100.0％

再現率：50.0％

F値：66.7％

カテゴリー:「IT・科学」の

適合率：69.2％

再現率：90.0％

F値：78.2％

カテゴリー:「グルメ」の

適合率：83.3％

再現率：100.0％

F値：90.9％







## 評価バッチ(gunosy_data/test.py)がなぜ動かないのか
テストデータtestdata.csvにURLではなく、テキストを持たせることで解決されたと思う。
実行する際の注意点としては、test.pyはgunosy_dataフォルダ内のnaivebayes.pyと各種pickleファイルをimportしているので、gunosy_dataフォルダ内で実行しないとうまくいかない。
