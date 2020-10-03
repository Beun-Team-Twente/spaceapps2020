import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

MIN_MATCH_COUNT = 10


def get_rocket(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('pics/rocket.jpg', 0)  # the template

    # Find the SIFT points
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(gray, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)
    good = [m for m,n in matches if m.distance < 0.7*n.distance]

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        transform, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h, w = template.shape
        rocket_gray = cv2.warpPerspective(gray, transform, (w, h))
        rocket_rgb = cv2.warpPerspective(img, transform, (w, h))
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))

    return rocket_gray, rocket_rgb

def find_mask(img):
    (thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    h, w = im_bw.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    inv = cv2.bitwise_not(im_bw)

    cv2.floodFill(inv, mask, (0, 0), 255)

    # plt.imshow(im_bw, cmap='gray')
    # plt.title('Corners'), plt.xticks([]), plt.yticks([])
    # plt.show()
    return cv2.bitwise_not(im_bw + inv)


img = cv2.imread('pics/rocket_s1.jpeg')
template = cv2.imread('pics/rocket.jpg', 0)  # the template
rocket_gray, rocket_rgb = get_rocket(img)
rocket_rgb = cv2.cvtColor(rocket_rgb, cv2.COLOR_RGB2RGBA)

mask1 = find_mask(rocket_gray)
mask2 = find_mask(template)
mask1 = mask1*255

img = Image.fromarray(rocket_rgb)
# img = img.convert("RGBA")
mask = Image.fromarray(mask1)
# print(list(mask.getdata()))
# img = img.convert("RGBA")

# img.putalpha(mask1)
img.save("pics/new_rocket.png")


plt.imshow(mask1,cmap = 'gray')
plt.title('Corners'), plt.xticks([]), plt.yticks([])
plt.show()
# ret, thresh = cv2.threshold(mask1, 127, 255,0)
# print(thresh)
# ret, thresh2 = cv2.threshold(mask2, 127, 255,0)
contours1,hierarchy1 = cv2.findContours(mask1,2,1)
contours2,hierarchy2 = cv2.findContours(mask2,2,1)


ret = cv2.matchShapes(contours1[0],contours2[0],1,0.0)
print( ret )

