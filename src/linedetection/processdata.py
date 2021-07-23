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
            new_ls[element] = int(0)
        elif(float(new_ls[element]) >= -0.1 and float(new_ls[element]) < -0.05):
            new_ls[element] = int(1)
        elif(float(new_ls[element]) >= -0.15 and float(new_ls[element]) < -0.1):
            new_ls[element] = int(2)
        elif(float(new_ls[element]) >= -0.2 and float(new_ls[element]) < -0.15):
            new_ls[element] = int(3)
        elif(float(new_ls[element]) >= -0.25 and float(new_ls[element]) < -0.2):
            new_ls[element] = int(4)
        elif(float(new_ls[element]) >= -0.3 and float(new_ls[element]) <= -1.0):
            new_ls[element] = int(5)
    print(len(new_ls))
    for j in range(len(new_ls)):
        # print("picdata")
        # print(j)
        new_Array.append(shrinkpic(cv2.imread("./data/pic_" + str(j) + ".jpg")))
    print("len new array")
    print(len(new_Array))
    return new_Array, new_ls

def shrinkpic(pic_Array):
    temp_Array = []
    for zeile in range(400): 
        temp = zeile + 215
        # print(temp)
        # print(len(pic_Array))
        # print(zeile)
        temp_Array.append([])
        for pixel in range(len(pic_Array[temp])):
            # print(pic_Array[temp][pixel][0])
            temp_Array[zeile].append(pic_Array[temp][pixel][0])
    
    # print(temp_Array)
    return temp_Array

# a,b = picdata()
# print(a[1])
# print(len(a))

