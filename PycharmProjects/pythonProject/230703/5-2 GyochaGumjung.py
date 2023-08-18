# 2023 -7 12 수업

# 판다스로 CSV 데이터 읽기
import pandas as pd
wine = pd.read_csv('https://bit.ly/wine_cvs_data')

# 클래스 열을 타깃으로 사용, 나머지 열을 특성 배열에 저장
data = wine[['alchol','sugar','pH']].to_numpy()
target = wine['class'].to_numpy()

print(data.shape)
print(target.shape)

# 훈련 세트와 테스트 세트를 나누기 - 훈련세트의 입력 데이터와 타겟 데이터를 train_input과 train_target에 저장
from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2, random_state=42)

# 결정 트리 분류 클래스 지정
from sklearn.tree import DecisionTreeClassifier
dtclf = DecisionTreeClassifier()
dtclf.fit(train_input, train_target)

train_score =dtclf.score(train_input, train_target)
test_score = dtclf.score(test_input, test_target)

print(train_score)
print(test_score)

predValue = dtclf.predict([[9.4, 1.9, 3.51]])
print(predValue)

from sklearn.model_selection import cross_validate
scores = cross_validate(dtclf, train_input, train_target)
print(scores)

from sklearn.model_selection import StratifiedKFold

myfold = StratifiedKFold(n_splits=10, random_state=42, shuffle=True)
scores = cross_validate(dtclf, train_input, train_target, cv=myfold)
print(scores)


# 교차 검증 - 하이퍼파라미터 탐색을 수행
# 첫번째 매개변수로 그리드 서치를 수행할 모델 객체 전달, 두번째 매개변수에는 탐색할 모델의 매개변수와 값 전달
from sklearn.model_selection import GridSearchCV
parms = {"min_impurity_decrease":[0.0001, 0.0002, 0.0003, 0.0004, 0.0005]}
gv = GridSearchCV(DecisionTreeClassifier(random_state=42), parms, n_jobs=-1)

gv.fit(train_input, train_target)

dt = gv.best_estimator_
score = dt.score(train_input, train_target)

