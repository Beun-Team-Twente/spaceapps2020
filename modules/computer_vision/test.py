import cv2

img = cv2.imread('pics/rocket_s1.jpeg')

cv2.imshow('image', img)
# Maintain output window utill
# user presses a key
cv2.waitKey(0)

# Destroying present windows on screen
cv2.destroyAllWindows()