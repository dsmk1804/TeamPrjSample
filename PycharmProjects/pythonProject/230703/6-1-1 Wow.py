import cv2
import matplotlib.pyplot as plt

# b g r
dark = cv2.imread('plzip.jpg',cv2.IMREAD_COLOR)

print(dark.shape)
print(dark[100, 100])

dark[80:120,80:120] = [0,0,0]
roi = dark[30:60,100:120]
dark[0:30,0:20] = roi

plt.imshow(cv2.cvtColor(dark,cv2.COLOR_BGR2RGB))
plt.show()





# 실행 자체는 되는데 이건 뭐지 Invalid SOS parameters for sequential JPEG

