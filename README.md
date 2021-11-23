# アニメ検索ダッシュボード

このダッシュボードでは以下の検索が可能です
* 放映された時間軸から検索する
* 人気のアニメの検索をする
* キーワードからマッチしたアニメを検索する
* アニメを推薦する  

## 使い方
### 1. 環境

```  
$ pip install -r requirements.txt  
```  


### 2. Firebaseの設定コンフィグ
`firebase/<your config>.json`を取得したのちに作成します。
### 3. slackのurl設定
環境変数に`WEB_HOOK_URL`をキーにして設定します。  
### 4. コマンド実行  
  
```
$ python3 app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```  

  
  
`http://127.0.0.1:8050/`にアクセスします。