# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:30:44 2018

@author: seedp
"""

cate_list = ['가전·디지털', '식품·건강', '화장품·이미용']
import pandas as pd
df = pd.read_csv('clf.csv', index_col='name')
df[df.cate1==cate_list[0]][1:3]
df[df.cate1==cate_list[1]][1:3]
df[df.cate1==cate_list[2]][1:3]

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1, tokenizer=lambda x: list(x))
corpus = [name.decode('utf-8') for name in df.index]
print (corpus[0])
analyze = vectorizer.build_analyzer()

analyze(u'삼육 두유')

X = vectorizer.fit_transform(corpus)
for el in cate_list:
    print (el)

for el in df.cate1[:3].tolist():
    print (el)
    
Y = map(cate_list.index, df.cate1.tolist())

print (X.shape[0], len(Y))

from sklearn.svm import LinearSVC
clf = LinearSVC(C=1.0)
clf.fit(X[:-200], Y[:-200])

from sklearn.metrics import accuracy_score
P = clf.predict(X[-200:])
print (accuracy_score(Y[-200:], P) * 100)

print (cate_list[clf.predict(vectorizer.transform([u'자동 물걸레 청소기']))[0]])
print (cate_list[clf.predict(vectorizer.transform([u'에센스 커버 팩트 리미티드 패키지']))[0]])
print (cate_list[clf.predict(vectorizer.transform([u'야생 블루베리 무려 10박스']))[0]])



