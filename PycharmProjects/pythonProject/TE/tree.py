# 264쪽에 나오는 csv 파일 그림을 정형 데이터라고 부름
# 정형 데이터 - 어떤 구조로 되어있다. CSV나 데이터베이스, 엑셀에 저장하기 쉬움
# NoSQL 데이터베이스는 엑셀이나 CSV에 담기 어려운 텍스트나 JSON 데이터를 저장하는데 용이하다.
# ex: 텍스트 데이터, 사진, 음악, 동영상 등
# ↑ 이거 정처기에 나오니까 잘 외워놔~
# 앙상블 학습: 정형 데이터를 가장 잘 다루는 알고리즘 ( 비정형은 신경망 알고리즘)
# 랜덤 포레스트 - 앙상블 학습의 대표격 - 나무를 말고 숲을 봐!

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

wine = pd.read_csv('https://bit.ly/wine_csv_data')

data = wine[['alcohol', 'sugar', 'pH']].to_numpy()
target = wine['class'].to_numpy()

train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_jobs=-1, random_state=42)
scores = cross_validate(rf, train_input, train_target, return_train_score=True, n_jobs=-1)

rfclf = RandomForestClassifier(n_jobs=-1, random_state=42)
rfclf.fit(train_input, train_target)

# print(np.mean(scores['train_score']), np.mean(scores['test_score']))
#
# scores = cross_validate(RandomForestClassifier(), train_input, train_target, return_train_score=True)
# print(scores)
#
# scores = cross_validate(ExtraTreesClassifier(), train_input, train_target, return_train_score=True)
# print(scores)
#
# scores = cross_validate(HistGradientBoostingClassifier(), train_input, train_target, return_train_score=True)
# print(scores)
#
# scores = cross_validate(GradientBoostingClassifier(), train_input, train_target, return_train_score=True)
# print(scores)
#
# scores = cross_validate(LGBMClassifier(), train_input, train_target, return_train_score=True)
# print(scores)
#
# scores = cross_validate(XGBClassifier(), train_input, train_target, return_train_score=True)
# print(scores)



