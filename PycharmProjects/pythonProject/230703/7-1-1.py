# 타겟값들
# 0 1 2 3 4 5 6 7 8 9
# 티셔츠 바지 스웨터 드레스 코트 샌달 셔츠 스니커즈 가방 영글부츠(순서대로)

from tensorflow import keras
from sklearn.model_selection import train_test_split

(train_input, train_target), (test_input, test_target) = keras.datasets.fashion_mnist.load_data()

train_scaled, val_scaled, train_target, val_target = train_test_split(
    train_scaled, train_target, test_size=0.2, random_state=42)

print(train_input.shape)
print(val_input.shape)

