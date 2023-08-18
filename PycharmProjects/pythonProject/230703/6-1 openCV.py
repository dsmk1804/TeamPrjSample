import cv2
import matplotlib.pyplot as plt

dark = cv2.imread("plzip.jpg", cv2.IMREAD_COLOR)

plt.imshow(cv2.cvtColor(dark,cv2.COLOR_BGR2RGB))
plt.scatter([10,20,30],[40,50,60])
plt.show()

import numpy as np

test = np.array([
    [ 0,0,1,0,0]
    

])