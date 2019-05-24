import numpy as np
import cv2

def cut(img):
    a = cv2.imread('./bg.png')
    d=np.zeros(a.shape)
    np.logical_and(a, img,d)
    result = img.copy()
    result[d[:,:,1] != 1] = (255, 255, 255)
    return result

def morphologytrans(img, kernalsize):
    kernel = np.ones((kernalsize, kernalsize), np.uint8)
    a = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    kernel1 = np.ones((kernalsize, kernalsize), np.uint8)
    a = cv2.erode(a, kernel1, iterations=1)
    return a

def background_init():
    fgbg = cv2.bgsegm.createBackgroundSubtractorGSOC()
    return fgbg

def process(fgbg,frame_lwpCV,count,step):
    if count%step == 0:

        fgmask = fgbg.apply(frame_lwpCV)
        diff = morphologytrans(fgmask, 10)

    else:
        diff = 0
    return diff


