import os

import numpy as np
import cv2

import matplotlib.pyplot as plt

from skimage.segmentation import felzenszwalb
import sim_features as sf
import ssearch

from color_utils import convert_colorspace
from segment_image import *
from inpainter import Inpainter
from skimage.restoration import inpaint

def inpaint_image(image,mode,p1,p2):
    print mode
    print image.shape
    if mode=='ss':
        image = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB)
        size = 15
        print 'blobbing'
        blob_array = segment_image(image)
        pixel_val_1 = np.array([p1[1],p1[0]])
        pixel_val_2 = np.array([p2[1],p2[0]])
        obs = []
        min_dist = [10000000000000]*5
        target = [None]*5
        print 'selecting'
        for blob in blob_array:
            x1,y1,x2,y2 =  blob.bbox
            dist = abs(x1-pixel_val_1[0])+abs(y1-pixel_val_1[1])+abs(x2-pixel_val_2[0])+abs(y2-pixel_val_2[1])
            for i,m in enumerate(min_dist):
                if m>dist and blob_check(blob,pixel_val_1,pixel_val_2):
                    min_dist[i] = dist
                    target[i] = blob

        image_copy,mask =blob_plot(image,target[-1])

        #dst = cv2.inpaint(image_copy,mask,3,cv2.INPAINT_TELEA)
        inp = Inpainter(image,mask*255,4)
        inp.inpaint()
        dst = inp.result
        dst = cv2.cvtColor(
            dst, cv2.COLOR_BGR2RGB)
        return dst

    elif mode =='gc':
        img = image
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (p1[0],p1[1],p2[0],p2[1])
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img2 = img*mask2[:,:,np.newaxis]
        img = img-img2
        # dst = inpaint.inpaint_biharmonic(img,mask2,multichannel =True)
        #dst = cv2.inpaint(img,mask2,3,cv2.INPAINT_TELEA)
        inp = Inpainter(image,mask*255,4)
        inp.inpaint()
        dst = inp.result
        return dst
