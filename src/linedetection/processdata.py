import cv2
import numpy as np
import sys
new_Array = []

num_Pics = 2
new_ls = []

def picdata():
    x, new_ls = np.loadtxt("./data/textdatei.txt", skiprows=0, unpack=True)
    for element in range(len((new_ls))):
        if(float(new_ls[element]) < 0.05 and float(new_ls[element]) >= -0.05):
            new_ls[element] = int(5)
        elif(float(new_ls[element]) >= 0.05 and float(new_ls[element]) < 0.2):
            new_ls[element] = int(6)
        elif(float(new_ls[element]) >= 0.2 and float(new_ls[element]) < 0.4):
            new_ls[element] = int(7)
        elif(float(new_ls[element]) >= 0.4 and float(new_ls[element]) < 0.6):
            new_ls[element] = int(8)
        elif(float(new_ls[element]) >= 0.6 and float(new_ls[element]) < 0.8):
            new_ls[element] = int(9)
        elif(float(new_ls[element]) >= 0.8 and float(new_ls[element]) <= 1.0):
            new_ls[element] = int(10)
        elif(float(new_ls[element]) >= -0.2 and float(new_ls[element]) < -0.05):
            new_ls[element] = int(4)
        elif(float(new_ls[element]) >= -0.4 and float(new_ls[element]) < -0.2):
            new_ls[element] = int(3)
        elif(float(new_ls[element]) >= -0.6 and float(new_ls[element]) < -0.4):
            new_ls[element] = int(2)
        elif(float(new_ls[element]) >= -0.8 and float(new_ls[element]) < -0.6):
            new_ls[element] = int(1)
        elif(float(new_ls[element]) >= -1.0 and float(new_ls[element]) < -0.8):
            new_ls[element] = int(0)
    # print(len(new_ls))
    for j in range(len(new_ls)):
        # print("picdata")
        print(j)
        new_Array.append(shrinkpic(cv2.imread("./data/pic_" + str(j) + ".jpg")))
    return new_Array, new_ls

def shrinkpic(pic_Array):
    temp_Array = []
    for zeile in range(len(pic_Array)):
        # print(pic_Array)
        # print(zeile)
        temp_Array.append([])
        for pixel in range(len(pic_Array[zeile])):
            # print(pixel)
            temp_Array[zeile].append(pic_Array[zeile][pixel][0])
    return temp_Array

a, b = picdata()
# print(a[1])
print(b)