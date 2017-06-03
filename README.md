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
          * testdata.xlsx
          * trainingdata.xlsx
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
* trainingdata.xlsx:教師データ
* testdata.xlsx:テストデータ
* training.py：学習用ソースコード。trainingdata.xlsxを用いて事後確率などを求め、それを種々のpickleファイルに保存する。
* naivebayes.py:webフォームから入力されたURLをナイーブベイズにより文書分類する。
* test.py:testdata.xlsxを用いて分類器の精度を検証する。


## セットアップの方法
* homework_gunosy\django\mysite\manage.pyを実行  
* http://127.0.0.1:8000/gunosy/get/　にアクセス  
* 記事のURLを入力（例えば　https://gunosy.com/articles/aYAZ2）し、送信ボタンを押すとカテゴリが出力される




## 分類器の精度
gunosy_dataフォルダ内のtestdata.xlsxを精度測定用のテストデータとして用いる。  
「正答率」＝「推定器で正しく分類できたデータの数」÷「テストデータの総数」として考える。  
訓練データを各カテゴリにつき２０～２５個の計１８０個、テストデータを各カテゴリにつき１０個の計８０個とした場合、正答率は77.5%であった。





## 評価バッチがなぜ動かないのか
testdata.xlsxには各カテゴリーの記事のURLが入力されている。精度をテストするときはそのURLからグノシーの記事本文を取得するのだが、グノシーの記事は削除されるのが早く、testdata.xlsxに入力してあるURLが数日でなくなってしまうことがある。URLが消えてしまうと当然本文を取得することができなくなり、エラーが起きると思われる。

## 動かすための解決策
testdata.xlsxから、本文の削除されたURLを除外する。（しかしまた数日するとエラーになる、、。）
