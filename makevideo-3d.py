from moviepy.editor import *
import cv2
import numpy as np  
from moviepy.audio.fx import all
from moviepy.video.fx.all import crop
from matplotlib import pyplot as plt
import os
import glob
from natsort import natsorted

frame_dir = './frames/'
left_frame_dir = './leftframes/'
right_frame_dir = './rightframes/'
d3eye_frame_dir = './3deyed/'


def get_all_file(path):
    for root, dirs, files in os.walk(path):  
        return files 

# 修改图片尺寸
def resize_image(image, width,height):
    dim = (width, height)
    resize_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resize_image

def jpg2png(img,op):
    r_channel, g_channel, b_channel = cv2.split(img) 

    img_RGBA = np.insert(
        img,
        3,         #position in the pixel value [ r, g, b, a <-index [3]  ]
        op,         # or 1 if you're going for a float data type as you want the alpha  to be fully white otherwise the entire image will be transparent.
        axis=2,    #this is the depth where you are inserting this alpha channel into
    )
#     print(cv2.split(img))
    return img_RGBA
#  scp zhz1.mp4 ubuntu@139.155.179.142:/home/ubuntu/superbrain/bletest/public
# width2d,height2d = 1954,1080

if __name__ == '__main__':
    frame_result = './frames/'

    filename = 'pngMask.png'
    width2d,height2d = 1958,1080
    width2d,height2d = 2478,1125
    frame_dir = './frames/'
    d3eye_dir = './3deyed/'
    sbs_dir = './sbs/'
    gif_name = 'frame_'
    fps = 30

    #read all files from directory
    files = get_all_file(frame_dir)
    counter = 0

    width3d,height3d = int(width2d/2),height2d
    maskname = 'pngMask.png'
    mask = cv2.imread(maskname,cv2.IMREAD_UNCHANGED)

    for filename in files:
        print('filename is :',frame_dir + filename)
        img_RGBA = cv2.imread(frame_dir + filename,cv2.IMREAD_UNCHANGED)
        height, width, channels = img_RGBA.shape
        # print('filename shape is :',img_RGBA.shape)

        img_3DRGBA = np.zeros((height3d, width3d, 4), dtype=np.uint8)
        img_3DRGBA[:,0:width3d-1] = img_RGBA[:,0:width3d-1]  #img1 
        # img2[:,0:newWidth-1] = img_RGBA[:,lfoffset:newWidth+lfoffset-1] #img2 is offset of lmg1
    # 读取mask，与image merge
        img_RGBA = resize_image(img_3DRGBA,width2d,height2d)
        # img_RGBA = cv2.addWeighted(img_RGBA, 1, mask, 1, 0)
        img_RGBA = cv2.bitwise_or(img_RGBA, mask, mask = None)

        offset = width        
        lfoffset = 8      # 左右图的offset 
        newWidth = int(offset-lfoffset) # new width of image

        img1 = np.zeros((height, width, 4), dtype=np.uint8)
        img2 = np.zeros((height, width, 4), dtype=np.uint8)

        img1[:,0:newWidth-1] = img_RGBA[:,0:newWidth-1]  #img1 
        img2[:,0:newWidth-1] = img_RGBA[:,lfoffset:newWidth+lfoffset-1] #img2 is offset of lmg1

        # img3d = img1+img2
        img3d = cv2.bitwise_and(img1, img2, mask = None)
        cv2.imwrite(sbs_dir + filename.replace("jpg","png")  , img3d)
        # print('preprocess done! ', filename.replace("jpg","png"))