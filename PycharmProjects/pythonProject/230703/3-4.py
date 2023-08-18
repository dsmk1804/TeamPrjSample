from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


train_data = np.array([[2,5],[3,6],[4,8],[5,10],[6,13]])
test_data = ([[3,7],[2,9],[5,11]])
target = np.array([10,18,32,50,78])

lr = LinearRegression()
lr.fit(train_data, target)

predTrain = lr.predict(train_data)
predTest = lr.predict(test_data)

print(predTrain)
print(predTest)

poly = PolynomialFeatures(include_bias=False, degree=5)
poly.fit(train_data)
train_poly = poly.transform(train_data)
print(train_poly)

lr = LinearRegression()
lr.fit(train_poly, target)

predTrain = lr.predict(train_poly)
predTest = lr.predict(test_poly)

print(predTrain)
print(predTest)