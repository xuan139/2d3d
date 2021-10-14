import os
import glob
from natsort import natsorted
from moviepy.editor import *
import cv2
import numpy as np  
from matplotlib.pyplot import imshow
import datetime
import time

# 修改图片尺寸
def resize_image(image, width,height):
    dim = (width, height)
    resize_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resize_image

def drawblock(img,x1,y1,c,op):
    height, width, channels = img.shape
    i=0  #op是透明度
    while i<height-1:
        if (i)%4==0:  #每隔4画一次
            if y1<width-1 and x1+i <height-1: #每次画2个点
                img[x1+i,y1]= [c,c,c,op]
                img[x1+i+1,y1]= [c,c,c,op]
        i=i+4   

def drawcolumn(img,x1,y1,c,op):
    for i in range(4):
        drawblock(img,x1+i,y1+i,c,op)

def setalpha(img,alphaValue):
    b_channel, g_channel, r_channel,alpha_channel = cv2.split(img)
    #print(alpha_channel) # alpha_channel[:, :int(b_channel.shape[0] / 2)] = 100 设置一些区域为透明值
    alpha_channel[:,:]=alphaValue  #所有区域设置透明值
    img_BGRA  = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return img_BGRA


def jpg2png(img,op):
    r_channel, g_channel, b_channel = cv2.split(img) 

    img_RGBA = np.insert(
        img,
        3,         #position in the pixel value [ r, g, b, a <-index [3]  ]
        op,         # or 1 if you're going for a float data type as you want the alpha  to be fully white otherwise the entire image will be transparent.
        axis=2,    #this is the depth where you are inserting this alpha channel into
    )
    return img_RGBA


#制作mask 
filename = 'pngMask.png'
width2d,height2d = 2478,1126
# width2d,height2d = 1958,1080
pngMask = np.zeros((height2d,width2d,4), dtype=np.uint8)
pngMask.fill(0)
pngMask = setalpha(pngMask,255) # 设为不透明
print('pngMask shape',pngMask.shape)
height, width, channels = pngMask.shape

print(channels)
# 45度角打码
j= 0-height
for i in range(0,width,4):
    j=j+1
    if j>height:
        j=0
    drawcolumn(pngMask,j,i,255,0) # 白色不透明
cv2.imwrite(filename, pngMask)