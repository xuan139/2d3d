import os
import glob
from natsort import natsorted
from moviepy.editor import *
import cv2
import numpy as np  
from matplotlib.pyplot import imshow
import datetime
import time

import multiprocessing as mp

#在图img的指定位置画点，c代表颜色，op代表透明度
def drawblock(img,x1,y1,c,op):
    height, width, channels = img.shape
    i=0  #op是透明度
    while i<height-1:
        if (i)%4==0:  #每隔4画一次
            if y1<width-1 and x1+i <height-1: #每次画2个点
                img[x1+i,y1]= [c,c,c,op]
                img[x1+i+1,y1]= [c,c,c,op]
        i=i+4   

#在图的指定位置x1,y1画线
def drawcolumn(img,x1,y1,c,op):
    for i in range(4):
        drawblock(img,x1+i,y1+i,c,op)

# 修改图片尺寸
def resize_image(image, width,height):
    dim = (width, height)
    resize_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resize_image

def setalpha(img,alphaValue):
    b_channel, g_channel, r_channel,alpha_channel = cv2.split(img)
    #print(alpha_channel) # alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100 设置一些区域为透明值
    alpha_channel[:,:]=alphaValue  #所有区域设置透明值
    img_BGRA  = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return img_BGRA


#把jpg转换为png
def jpg2png(img,op):
    r_channel, g_channel, b_channel = cv2.split(img) 

    img_RGBA = np.insert(
        img,
        3,         #position in the pixel value [ r, g, b, a <-index [3]  ]
        op,        # or 1 if you're going for a float data type as you want the alpha  to be fully white otherwise the entire image will be transparent.
        axis=2,    #this is the depth where you are inserting this alpha channel into
    )
    return img_RGBA


def mergeto3d(imgl,imgr,distance):
    b_channel, g_channel, r_channel,alpha_channel = cv2.split(imgl)
    # print('imgl alpha_channel is ',alpha_channel)
    print('imgl ',imgl.shape)
    combined_img = imgl.copy()
    for i in range(len(combined_img)):
        for j in range(len(combined_img[i]) - distance):
            if combined_img[i][j][3]==0:
                print ('i,j,combined_img[i][j][3]==0,imgr[i][j + distance][3]',i,j,combined_img[i][j][3],imgr[i][j + distance][3])
                # print ('------ i,j,combined_img[i][j][0],imgr[i][j + distance][3]',i,j,combined_img[i][j][0],imgr[i][j + distance][0])
                # print ('------ i,j,combined_img[i][j][1],imgr[i][j + distance][3]',i,j,combined_img[i][j][1],imgr[i][j + distance][1])
                # print ('------ i,j,combined_img[i][j][2],imgr[i][j + distance][3]',i,j,combined_img[i][j][2],imgr[i][j + distance][2])
                combined_img[i][j][0] = imgr[i][j + distance][0]
                combined_img[i][j][1] = imgr[i][j + distance][1]
                combined_img[i][j][2] = imgr[i][j + distance][2]
                combined_img[i][j][3] = imgr[i][j + distance][3]
    return combined_img


if __name__ == '__main__':

    start_t = datetime.datetime.now()
    num_cores = int(mp.cpu_count())
    print("本地计算机有: " + str(num_cores) + " 核心")

    filename = '21097.jpg'
    width2d,height2d = 1958,1080
    width2d,height2d = 2478,1125
    # An alpha value of zero represents full transparency, 
    # and a value of (2^bitdepth)-1 represents a fully opaque pixel. 
    # Intermediate values indicate partially transparent pixels that 
    # can be combined with a background image to yield a composite image. 
    # (Thus, alpha is really the degree of opacity of the pixel.

    # 转换2d图片为3d图片PART1 
    # 1.把2d图 resize width 
    # 2.目前手机为1920*1080 目前测试结果是把size1920*1080 宽度放到1956,1080为最佳3D效果
    # 3.把2d图jpg格式转换为png格式

    img = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
    print(filename)
    height, width, channels = img.shape
    print('jpg img shape is ',img.shape)

    img = resize_image(img,width2d,height2d)
    height, width, channels = img.shape

    #把jpg转换为png ，透明度为255 完全不透明
    if channels==3:
        img_RGBA = jpg2png(img,255)
    else:
        img_RGBA = setalpha(img,255)

    print('png img_RGBA shape is',img_RGBA.shape)
    height, width, channels = img_RGBA.shape
    print('image is resize and convert into png format done!')

    maskname = 'pngMask.png'
    mask = cv2.imread(maskname,cv2.IMREAD_UNCHANGED)
    # 读取mask，与image merge
    img_RGBA = cv2.bitwise_or(img_RGBA, mask, mask = None)
    cv2.imwrite('img_RGBA.png', img_RGBA)



    # print('width is',width)
    # # 45度角打码 img_RGBA = jpg2png(img,255) 完全不透明

    # j= 0-height
    # for i in range(0,int(width),4):
    #     j=j+1
    #     if j>height:
    #         j=0
    #     drawcolumn(img_RGBA,j,i,255,255) # 白色透明

    # cv2.imwrite('img_RGBA.png', img_RGBA)



    offset = width        
    lfoffset = 8      # 左右图的offset 
    newWidth = int(offset-lfoffset) # new width of image
    
    img1 = np.zeros((height, width, 4), dtype=np.uint8)
    img2 = np.zeros((height, width, 4), dtype=np.uint8)

    img1[:,0:newWidth-1] = img_RGBA[:,0:newWidth-1]  #img1 
    img2[:,0:newWidth-1] = img_RGBA[:,lfoffset:newWidth+lfoffset-1] #img2 is offset of lmg1
    # result = img1+img2 
    result = cv2.bitwise_and(img1, img2, mask = None)
    cv2.imwrite('3d' + str(lfoffset) +'.png', result)
    print('3d' + str(lfoffset) +'.png')


