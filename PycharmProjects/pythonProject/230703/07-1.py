# 인공 신경망
# 텐서플로와 관련 있다. - 딥 러닝 라이브러리
import tensorflow as tf

tf.keras.utils.set_random_seed(42)
tf.config.experimental.enable_op_determinism()

#패션 MNIST
from tensorflow import keras

(train_input, train_target), (test_input, test_target) = keras.datasets.fashion_mnist.load_data()

print(train_input.shape, train_target.shape)

print(test_input.shape, test_target.shape)

import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 10, figsize=(10,10))
for i in range(10):
    axs[i].imshow(train_input[i], cmap='gray_r')
    axs[i].axis('off')
plt.show()

# 타겟값들
# 0 1 2 3 4 5 6 7 8 9
# 티셔츠 바지 스웨터 드레스 코트 샌달 셔츠 스니커즈 가방 영글부츠(순서대로)

print([train_target[i] for i in range(10)])

import numpy as np

print(np.unique(train_target, return_counts=True))

# 로지스틱 회귀로 패션 아이템 분류하기
train_scaled = train_input / 255.0
train_scaled = train_scaled.reshape(-1, 28*28)

print(train_scaled.shape)

from sklearn.model_selection import cross_validate
# ↑ 교차검증
from sklearn.linear_model import SGDClassifier
# ↑ 클래스 분류 - 확률적 분석

sc = SGDClassifier(loss='log_loss', max_iter=5, random_state=42)

scores = cross_validate(sc, train_scaled, train_target, n_jobs=-1)
print(np.mean(scores['test_score']))

# 인공신경망 - 텐서플로와 케라스
from tensorflow import keras
from sklearn.model_selection import train_test_split

train_scaled, val_scaled, train_target, val_target = train_test_split(
    train_scaled, train_target, test_size=0.2, random_state=42)

print(train_scaled.shape, train_target.shape)

print(val_scaled.shape, val_target.shape)

dense = keras.layers.Dense(10, activation='softmax', input_shape=(784,))
model = keras.Sequential(dense)

# 인공 신경망으로 패션 아이템 분류하기
model.compile(loss='sparse_categorical_crossentropy', metrics='accuracy')

print(train_target[:10])

model.fit(train_scaled, train_target, epochs=5)

model.evaluate(val_scaled, val_target)

