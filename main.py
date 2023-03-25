#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import  numpy as np
global ori_img,ir_img,color_img,point,count,filename
import  os
from numpy.linalg import inv
import platform
count = 0
point ={}
new_path = '/home/lishuai/code/labelhomography/dataset'



def img_perspect_transform(img, M):
    img_size = (img.shape[1], img.shape[0])
    return cv2.warpPerspective(img, M, img_size)

def on_mouse(event,x,y,flags,param):
    global color_img,ir_img,ori_img,point,count,filename
    # img=ori_img.copy()
    if event==cv2.EVENT_LBUTTONDOWN:#左键点击
        count = count+1
        if count %2 ==0:
            point[count-1]=(x,y)
            cv2.circle(ori_img,point[count-1],10,(0,255,0),5)
        else:
            point[count-1]=(x,y)
            cv2.circle(ori_img, point[count-1], 10, (0, 255, 0), 5)
        cv2.imshow(filename,ori_img)


    elif event==cv2.EVENT_LBUTTONUP:#左键释放
        if count %2 ==0:
            print("point1 to point2",point[count-2],point[count-1])
            cv2.line(ori_img,point[count-2],point[count-1],(0,0,255),3)
            cv2.imshow(filename, ori_img)
        if count % 8 == 0:

            four_points = [(point[count - 7][0]-384,point[count - 7][1]),(point[count - 5][0]-384,point[count - 5][1]),
                           (point[count - 3][0]-384,point[count - 3][1]),(point[count - 1][0]-384,point[count - 1][1])]     #红外图
            pre_four_points = [point[count-8],point[count-6],point[count-4],point[count-2]]     #原图
            H = cv2.getPerspectiveTransform(np.float32(four_points), np.float32(pre_four_points))
            H_inverse = inv(H)    #求逆矩阵
            warped_image = img_perspect_transform(color_img,H_inverse)
            combine = cv2.addWeighted(ir_img,0.8,warped_image,0.4,0)
            training_image = np.dstack((color_img,warped_image))
            H_four_points = np.subtract(np.array(pre_four_points), np.array(four_points))
            datum = (training_image, np.array(four_points), H_four_points)
            print(datum)
            # cv2.imshow("perspect",combine)
            print(H)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            np.save(new_path + '/' + ('%s' % int(count/8)).zfill(6), datum)

def read_path(file_pathname,mode = 'gray'):
    color_filepath = file_pathname + '/color'
    ir_filepath = file_pathname + '/ir'
    #遍历该目录下的所有图片文件
    global ori_img, ir_img, color_img, filename
    for filename in os.listdir(color_filepath):

        if mode == 'gray':
            color_img = cv2.imread(color_filepath+'/'+filename,0)
            ir_img = cv2.imread(ir_filepath+'/'+filename,0)
        elif mode == 'color':
            color_img = cv2.imread(color_filepath + '/' + filename)
            ir_img = cv2.imread(ir_filepath + '/' + filename)
        else:
            print("please set mode == gray or mode == color")
            return -1
        cv2.namedWindow(filename)
        cv2.setMouseCallback(filename,on_mouse)
        ori_img = np.hstack((color_img,ir_img))
        cv2.imshow(filename,ori_img)
        if platform.system().lower() == 'windows':
            print("current platform is windows")
            cv2.waitKey(0)
        elif platform.system().lower() == 'linux':
            print("current platform is linux")
            while cv2.waitKey(100) != 27:
                if cv2.getWindowProperty(filename, cv2.WND_PROP_VISIBLE) <= 0:
                    break


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    read_path("./Image",mode='gray')


