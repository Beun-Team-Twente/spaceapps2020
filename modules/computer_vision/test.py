import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pics/rocket.jpg', 0)
kernel_size = 15
gray = cv2.GaussianBlur(img,(kernel_size, kernel_size),0)

low_threshold = 100
high_threshold = 150
edges = cv2.Canny(gray, low_threshold, high_threshold)

dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
kernel = np.ones((5,5),np.uint8)
dst = cv2.dilate(dst,kernel)
# Threshold for an optimal value, it may vary depending on the image.
# img[dst>0.01*dst.max()]=[0,0,255]
kernel = np.ones((5,5),np.uint8)

plt.imshow(dst,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(dst,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()