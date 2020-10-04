import cv2
import numpy as np
# from matplotlib import pyplot as plt
from PIL import Image
import os

from . import conversions

MIN_MATCH_COUNT = 10


def get_rocket(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(os.path.join(os.path.dirname(__file__), 'pics/rocket.jpg'), 0)  # the template

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
    # Get binary image
    (thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Get mask and inverse of image
    h, w = im_bw.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    inv = cv2.bitwise_not(im_bw)

    # Fill the background
    im_flood_fill = inv.astype("uint8")
    cv2.floodFill(im_flood_fill, mask, (0, 0), 255)

    # Combine the two images to obtain a 'mask'
    combo = cv2.bitwise_and(im_bw, im_flood_fill)


    # Find the contour of the rocket ship, the largest is the border
    contours, hierarchy = cv2.findContours(combo, 2, 1)
    sorted_list = list(sorted(contours, key=len))

    # Check size of contour
    for c in sorted_list:
        mask = np.zeros((h, w), np.uint8)
        rocket_mask = cv2.drawContours(mask, [c], 0, 255, thickness=cv2.FILLED)
        area = np.sum(rocket_mask) / 255
        if 207037*1.1 >= area >= 207037*0.9:
            # Print only the rocket contour
            return rocket_mask

    print("No proper contour has been found, please try again!")
    return None


def save_wo_background(img):
    rocket_gray, rocket_rgb = get_rocket(img)
    rocket_rgb = cv2.cvtColor(rocket_rgb, cv2.COLOR_BGR2BGRA)
    mask = find_mask(rocket_gray)

    if mask == None: # No contours found
        return None

    rocket_rgb[:, :, 3] = mask
    return conversions.opencv_to_pil(rocket_rgb)

def run(pil_img):
    # Run the algorithm on a PIL image
    img = conversions.pil_to_opencv(pil_img)
    return save_wo_background(img)
