#### testing function
import cv2
import numpy as np
import os

from . import conversions

def astronaut_face_adder(image):
    astronaut = cv2.imread(os.path.join(os.path.dirname(__file__), 'pics/astronaut.png'))  # the template
    rocket = cv2.imread(os.path.join(os.path.dirname(__file__), 'pics/rocket.jpg'))  # the template
    astronaut_copy = cv2.imread(os.path.join(os.path.dirname(__file__), 'pics/astronaut.png'), cv2.IMREAD_UNCHANGED)
    output = np.zeros(rocket.shape)
    output2 = astronaut.copy()
    output3 = np.zeros(astronaut.shape)
    gray = cv2.cvtColor(rocket, cv2.COLOR_BGR2GRAY)
    gray_astronaut = cv2.cvtColor(astronaut, cv2.COLOR_BGR2GRAY)

    # find circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20)
    circles_astronaut = cv2.HoughCircles(gray_astronaut, cv2.HOUGH_GRADIENT, 1, 40)

    # create circle mask around face astronaut
    circles_astronaut = np.round(circles_astronaut[0, :]).astype("int")
    x_astronaut = circles_astronaut[0, 0]
    y_astronaut = circles_astronaut[0, 1]
    r_astronaut = circles_astronaut[0, 2]
    output3[y_astronaut - r_astronaut:y_astronaut + r_astronaut, x_astronaut - r_astronaut:x_astronaut + r_astronaut,
    :] = np.array([255, 255, 255])

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

            # Floodfill from point (0, 0)
            cv2.floodFill(im_floodfill, mask, (0, 0), 255)

            # Invert floodfilled image
            im_floodfill_inv = cv2.bitwise_not(im_floodfill)


            # Combine the two images to get the foreground
            im_out = cv2.bitwise_or(im_th.astype(int),im_floodfill_inv.astype(int))

            # replace im_out with face
            rows,cols = np.where(im_out[:, :, 0] == 0)
            im_out[rows, cols, :] = np.array([0, 0, 0])
            rows,cols = np.where(im_out[:,:,2] == 255)
            im_out[rows,cols,:] = image[rows,cols,:]
            im_out = im_out[min(rows):max(rows), min(cols):max(cols), :]

            # resize face to size face astronaut
            width = 2 * r_astronaut
            dim = (width, width)
            new_face = cv2.resize(im_out.astype("uint8"), dim, interpolation=cv2.INTER_AREA)

            # replace mask astronaut face with new face
            output3[y_astronaut - r_astronaut:y_astronaut + r_astronaut,
            x_astronaut - r_astronaut:x_astronaut + r_astronaut, :] = new_face

            # combine astronaut with mask astronaut
            grey_output3 = cv2.cvtColor(output3.astype("uint8"), cv2.COLOR_BGR2GRAY)
            rows, cols = np.where(grey_output3[:, :] != 0)
            astronaut[rows, cols, :] = output3[rows, cols, :]

            # make background transparant
            astronaut = cv2.cvtColor(astronaut, cv2.COLOR_BGR2BGRA)
            astronaut_copy = cv2.cvtColor(astronaut_copy, cv2.COLOR_BGR2BGRA)
            rows, cols = np.where(astronaut_copy[:, :, 3] == 0)
            astronaut[rows, cols, 3] = 0

        return astronaut

    else:
        return None

def run(pil_img):
    # Run the algorithm on a PIL image
    img = conversions.pil_to_opencv(pil_img)
    return conversions.opencv_to_pil(astronaut_face_adder(img))


# image = cv2.imread('pics/new_rocket3.png')
# testie = astronaut_face_adder(image)
# if testie is not None:
#     cv2.imshow("output", testie)
#     cv2.waitKey(0)
# else:
#     print('something went wrong')