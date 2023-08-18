import pandas as pd

# 데이터 불러오기
data = pd.read_csv('train.csv')
# print(data.head())
# print(data.columns)

# 데이터를 성별로 분류하기
# print(data['Sex'])
data['Sex'] = data['Sex'].map({'female':1, 'male':0})
# print(data['Sex'])

# 결측지 제거하기
data['Age'].fillna(value=data['Age'].mean(),inplace=True)

dummies = pd.get_dummies(data['Pclass'])
print(dummies)
# data 중에서 Pclass 데이터 삭제
del data['Pclass']
print(data.head())

data = pd.concat([data,dummies],axis=1, join='inner')
data.rename(columns={1:'FirstClass', 2:'SecondClass', 3:'ThirdClass'}, inplace=True)

print(data.head())

data['FirstClass'] = data['FirstClass'].map({False: 0, True: 1})
data['SecondClass'] = data['SecondClass'].map({False: 0, True: 1})
data['ThirdClass'] = data['ThirdClass'].map({False: 0, True: 1})


input_data = data[['age', 'sex', 'FirstClass', 'SecondClass', 'ThirdClass']]
target_data = data['Survived']

print(input_data[:5])
print(target_data[:5])

from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = \
    train_test_split(input_data, target_data, random_state=42)

print(train_input.shape)
print(test_input.shape)
print(train_target.shape)
print(train_input.shape)

from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(train_input)

train_scaled = ss.transform(train_input)
test_scaled = ss.transform(test_input)

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

lr = LogisticRegression()
lr.fit(train_scaled, train_target)

train_score = lr.score(train_scaled, train_target)
test_score = lr.score(test_scaled, test_target)

print(train_score)
print(test_score)

sclf = SGDClassifier(loss= 'log')
sclf.fit(train_scaled, train_target)

train_score = sclf.score(train_scaled, train_target)
test_score = sclf.score(test_scaled, test_target)

print(train_score)
print(test_score)

sclf.partial_fit(train_scaled, train_target)
train_score = sclf.score(train_scaled, train_target)
test_score = sclf.score(train_scaled, train_target)

print(train_score)
print(test_score)