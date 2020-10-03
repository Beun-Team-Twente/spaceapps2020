import numpy as np
from PIL import Image
import cv2

def pil_to_opencv(img):
    # Converts a PIL image to OpenCV format
    numpy_image = np.array(img) 
    return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 

def opencv_to_pil(img):
    # Converts an OpenCV image to the PIL format
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    im_pil = Image.fromarray(img, 'RGBA')
    return im_pil
