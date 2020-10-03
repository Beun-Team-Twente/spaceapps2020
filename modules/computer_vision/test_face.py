import cv2
import numpy as np
import matplotlib.pyplot as plt
import get_rocket_og
#%matplotlib inline

# read images
img1 = cv2.imread('pics/rocket_s1.jpeg')
img2 = cv2.imread('pics/rocket.jpg')
output = np.zeros(img2.shape)


gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15)
print(circles.shape)
# ensure at least some circles were found

if circles is not None:
    circles = np.round(circles[0,:]).astype("int")
    for(x,y,r) in circles:
        circleimg = cv2.circle(output, (x,y), r, (0, 255, 0), 4)
        ret, im_th = cv2.threshold(circleimg, 127, 255, 0)
        # Copy the thresholded image
        im_floodfill = im_th.copy().astype("uint8")

        # Mask used to flood filling.
        # NOTE: the size needs to be 2 pixels bigger on each side than the input image
        h, w = im_th.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        print(mask.shape)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255)

        # Invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        print(im_th.shape)
        print(im_floodfill_inv.shape)
        print(np.unique(im_th.astype(int)), np.unique(im_floodfill_inv))

        # Combine the two images to get the foreground
        im_out = cv2.bitwise_or(im_th.astype(int),im_floodfill_inv.astype(int))
        for x in range(im_out.shape[0]):
            for y in range(im_out.shape[1]):
                # print(type(y))
                #print(type(np.array([0, 255, 255])))
                if np.array_equal(im_out[x,y],np.array([0, 255, 255])):
                    im_out[x,y] = np.array([0, 0, 0])

        plt.subplot(121),plt.imshow(img2,cmap = 'gray')
        plt.subplot(122),plt.imshow(im_out,cmap = 'gray')
        plt.show()
        print(im_out)


    # cv2.imwrite('pics/maskie.png', im_out)
    # cv2.imshow("output", im_out.astype("uint8"))
    # cv2.waitKey(0)
