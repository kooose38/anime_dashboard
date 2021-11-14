import pandas as pd 
import numpy as np 
import scipy as sp 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from janome.tokenizer import Tokenizer

class Lang:
    def __init__(self, ser):
        self.ser = ser 
        self.word2index = {"<PAD>": 0, "<SEQ>": 1, "<EOS>": 2, "<UNK>": 3}
        self.index2word = {}
        self.len = 0 
        self.fit()

    def fit(self):
        for doc in self.ser:
            if self.len <= len(doc.split()):
                self.len = len(doc.split())
            for txt in doc.split():
                if txt not in self.word2index:
                    self.word2index[txt] = len(self.word2index)
        self.index2word = {v: k for k, v in self.word2index.items()} 

    def transform(self, doc):
        new = []
        new.append(self.word2index["<SEQ>"])
        for txt in doc.split():
            if txt in self.word2index:
                new.append(self.word2index[txt])
            else:
                new.append(self.word2index["<UNK>"])

        if len(new) < self.len:
            for _ in range(self.len - len(new)):
                new.append(self.word2index["<PAD>"])
        elif len(new) >= self.len:
            new = np.array(new)[:self.len].tolist()

        new.append(self.word2index["<EOS>"])
        return new 
    
    
def get_vector(df):
    j_t = Tokenizer()
    def make_wakati(doc):
        new = []
        for word in j_t.tokenize(doc, wakati=True):
            new.append(word)
        return " ".join(new)
    
    df["cln_title"] = df.title.apply(make_wakati)
    lang = Lang(df["cln_title"])
    df["token"] = df.cln_title.apply(lang.transform)
    
    v = []
    for arr in df.token.to_list():
        v.append(arr)
        del arr 
        
    title = sp.sparse.csr_matrix(v)
    del v 
    title = cosine_similarity(title)
    title = pd.DataFrame(title, columns=df.title, index=df.title)
    return title 