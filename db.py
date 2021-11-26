import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
import datetime 
import os 

# 環境変数を設定する
cred = credentials.Certificate(f"firebase/{os.environ['FIREBASE_KEY']}")
firebase_admin.initialize_app(cred)

db = firestore.client()

def request_post_db(uid, page, kwd):
    now = str(datetime.datetime.now()) 
    
    ref = db.collection(u"users").document(uid + now)
    ref.set({
        "uid": uid, 
        "created_at": now, 
        "page": page, 
        "keyword": kwd
    })
