# 감성분석
import re
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import warnings
import pickle
warnings.filterwarnings(action="ignore")

train_df = pd.read_csv("ratings_train.txt", encoding="utf8", sep="\t", engine="python")
train_df.head()
train_df.info()

# 데이터 정제
train_df = train_df[train_df["document"].notnull()]
train_df.info()

train_df["label"].value_counts()

train_df["document"] = train_df["document"].apply(lambda x: re.sub(r'[^ㄱ-ㅣ가-힇]+', " ", x))
# ㄱ, ㄴ, ..., ㅏ, ㅑ, ... ㅣ를 공백으로 치환
# re.sub = 덮어씌우는 것 // lambda = 콜백 함수 어떤 함수를 지속적으로 호출하고 싶을 때 사용. 인자(x)로 넘어감
# 문자 하나하나를 " "으로 대체하는 것
train_df.head()

okt = Okt()


def okt_tokenizer(text):
    tokens = okt.morphs(text) # 문장을 띄워쓰기 단위로 끊어줌
    return tokens


tfidf = TfidfVectorizer(tokenizer=okt_tokenizer, ngram_range=(1, 2), min_df=3, max_df=0.9)
tfidf.fit(train_df["document"])
train_tdf = tfidf.transform(train_df["document"])

sa_lr = LogisticRegression(random_state=0)
sa_lr.fit(train_tdf, train_df["label"])

params = {"C": [1, 3, 3.5, 4, 4.5, 5]}
sa_lr_gscv = GridSearchCV(sa_lr, param_grid=params, cv=3, scoring="accuracy", verbose=1)
sa_lr_gscv.fit(train_tdf, train_df["label"])

sa_lr_best = sa_lr_gscv.best_estimator_

test_df = pd.read_csv("ratings_test.txt", encoding="utf8", sep="\t", engine="python")
test_df = test_df[test_df["document"].notnull()]
test_df["label"].value_counts()
test_df["document"] = test_df["document"].apply(lambda x: re.sub(r'[^ㄱ-ㅣ가-힇]+', " ", x))
test_tdf = tfidf.transform(test_df["document"])

test_predict = sa_lr_best.predict(test_tdf)
print("감성분석 정확도: ", round(accuracy_score(test_df["label"], test_predict), 3))

st = "웃자 ^0^ 오늘은 좋은 날이 될 것 같은 예감 100%! ^^*"
st = re.compile(r'[ㄱ-ㅣ가-힇]+').findall(st)
print(st)
st = [" ".join(st)]
print(st)

st_tfidf = tfidf.transform(st)
st_predict = sa_lr_best.predict(st_tfidf)
print(st, "->", "부정" if st_predict == 0 else "긍정")

saved_tfidf = pickle.dumps(tfidf)
saved_best = pickle.dumps(sa_lr_best)

tf_file = open("tfidf.pkl", "wb")
tf_file.write(saved_tfidf)
tf_file.close()

bt_file = open("best.pkl", "wb")
bt_file.write(saved_best)
bt_file.close()

tf_file = open("tfidf.pkl", "rb")
tfidf2 = pickle.loads(tf_file.read())
tf_file.close()

bt_file = open("best.pkl", "rb")
best2 = pickle.loads(bt_file.read())
bt_file.close()

st = "안녕! 오늘은 날씨가 짜증나네!"
st = re.compile(r'[ㄱ-ㅣ가-힇]+').findall(st)
st = [" ".join(st)]

st_tfidf = tfidf2.transform(st)
st_predict = best2.predict(st_tfidf)
print(st, "->", "부정" if st_predict == 0 else "긍정")
