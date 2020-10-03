# This is a directory for the computer-vision modules

import cv2
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images
folder="C:\Users\melis\Documents\Prive\Nasa Space Apps\rocket1"
