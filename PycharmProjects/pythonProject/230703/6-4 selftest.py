import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

fruits = np.load('fruits_300.npy')
print(fruits.shape)

fruits_2d = fruits.reshape(-1, 100*100)
print(fruits_2d.shape)

pca = PCA(n_components=50)
pca.fit(fruits_2d)

print(pca.components_.shape)

주성분50개이미지 = pca.components_.reshape(-1, 100, 100)

fig, axs = plt.subplots(5, 10, squeeze=False)

for i in range(5):
    for j in range(10):
        axs[i,j].imshow(주성분50개이미지[i*10+j],cmap='gray_r')
        axs[i,j].axis('off')
plt.show()

fruits_pca = pca.transform(fruits_2d)
fruits_inverse = pca.inverse_transform(fruits_pca)

print(fruits_2d.shape)
print(fruits_pca.shape)
print(fruits_inverse.shape)

fruits_inverse = fruits_inverse.reshape(-1, 100, 100)

for i in range(20, 30):
    for j in range(10):
        axs[i,j].imshow(fruits_inverse[i*10+j],cmap='gray_r')
        axs[i,j].axis('off')
plt.show()

