import os

import numpy as np
import cv2

import matplotlib.pyplot as plt
import scipy.io
from skimage.segmentation import felzenszwalb
import sim_features as sf
import ssearch
from color_utils import convert_colorspace
from skimage.restoration import inpaint

def segment_image(image, color_space_list = ['HSV','LAB'],
                  ks = [50,100]):

    blob_array =[]
    priority = []
    seg_masks = []
    converted_images = convert_colorspace(image,color_space_list)
    sim_feats_list = [ sf.color_hist_sim(), sf.texture_hist_sim(),
                      sf.size_sim(image.shape), sf.fill_sim(image.shape) ]
    for img in converted_images:
        for j in ks:
            print("segmenting",j)
            segmented_mask = felzenszwalb(img,j,sigma = 0.8,
                                         min_size = j)
            print("blobbing",j)
            blobs = ssearch._ssearch(img,segmented_mask,sim_feats =
                                          sim_feats_list)
            blob_array.append(blobs)
            priority.append(
                np.arange(len(blobs),0,-1).clip(0,(len(blobs)+1)/2))
            seg_masks.append(segmented_mask)
    blob_array = ssearch.remove_duplicate(blob_array)
    return blob_array

def blob_plot(image,blob):
    mask = np.zeros(image.shape[:2]).astype(np.uint8)
    for x,y in blob.loc:
        image[x,y,:] = [0,0,0]
        mask[x,y] = 1
    return image, mask

def generate_blur(image,size):
    # generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size

    # applying the kernel to the input image
    output = cv2.filter2D(image, -1, kernel_motion_blur)
    return output

def blob_check(blob,p1,p2):
    for loc in list(blob.loc):
        if loc[0]<p1[0] or loc[0]>p2[0] or loc[1]<p1[1] or loc[1]>p2[1]:
            return False
    return True


if __name__ == '__main__':
    mode = 'gc'
    if mode=='ss':
        image = cv2.cvtColor(
            cv2.imread('test2.jpg'), cv2.COLOR_BGR2RGB)
        size = 15
        blurred = generate_blur(image,size)
        plt.imshow(image)
        plt.show()
        blob_array = segment_image(image)
        pixel_val_1 = np.array([81,25])
        pixel_val_2 = np.array([251,448])
        print image.shape
        obs = []
        min_dist = [10000000000000]*5
        target = [None]*5
        for blob in blob_array:
            x1,y1,x2,y2 =  blob.bbox
            dist = abs(x1-pixel_val_1[0])+abs(y1-pixel_val_1[1])+abs(x2-pixel_val_2[0])+abs(y2-pixel_val_2[1])
            for i,m in enumerate(min_dist):
                if m>dist and blob_check(blob,pixel_val_1,pixel_val_2):
                    min_dist[i] = dist
                    target[i] = blob

        blob_sizes = [tar.blob_size for tar in target]
        target = [x for _,x in sorted(zip(blob_sizes,target))]
        for x,y in target[-1].loc:
            blurred[x,y,:] = image[x,y,:]

        image_copy,mask =blob_plot(image,target[-1])
        dst = cv2.inpaint(image_copy,mask,3,cv2.INPAINT_TELEA)
        print image_copy[pixel_val_1[0],pixel_val_1[1],:]
        cv2.imwrite('1.jpg',cv2.cvtColor(image_copy,
                                    cv2.COLOR_RGB2BGR))
        cv2.imwrite('2.jpg',cv2.cvtColor(blurred,
                cv2.COLOR_RGB2BGR)) 
        cv2.imwrite('3.jpg',cv2.cvtColor(dst,
                cv2.COLOR_RGB2BGR))

    elif mode =='gc':
        img = cv2.imread('test2.jpg')
        plt.imshow(img)
        print img.shape
        plt.show()
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (81,35,255,422)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img2 = img*mask2[:,:,np.newaxis]
        img3 = generate_blur(img,15)
        img3 = img3-img3*mask2[:,:,np.newaxis]+img2
        img = img-img2
        print("inpainting")
        #dst = cv2.inpaint(img,mask2,3,cv2.INPAINT_TELEA)

        dst = inpaint.inpaint_biharmonic(img,mask2,multichannel =True)
        cv2.imwrite('1.jpg',img)
        cv2.imwrite('4.jpg',dst)
        cv2.imwrite('3.jpg',img3)

#code I did not want to delete
    #for blob in target:
    #    match = 0
    #    for loc in list(blob.loc):

    #        if (pixel_val_1==loc).all() or (pixel_val_2==loc).all():
    #            match+=1
    #            if match == 2:
    #                obs.append(blob)
    #                break

    #base_delta = 100000000000
    #target = obs[0]
    #for blob in obs:
    #    area_delta = abs(blob.blob_size-abs((
    #        pixel_val_1[0]-pixel_val_2[0])*(pixel_val_1[1]-pixel_val_2[1])))
    #    if base_delta>area_delta:
    #        target = blob
    #        base_delta = area_delta

