import random
import numpy as np
import numpy as reshape
import csv

np.set_printoptions(threshold=np.inf)
"""把data & label連在一起並且轉成CNN圖片格式寫入train.csv"""
x=[]
y=[]
size = np.array([[0]*13]*13) #二維資料
rrow=[]
roww=[]
all = []

print("reading file...")
with open(r'D:\Finish\dataset\x.csv', newline='') as csvfile:
    # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
    #rows = csv.DictReader(csvfile) #csv.DictReader可以資料查找 d = {key1: value1, key2: value2}
    rows = csv.reader(csvfile)
    data_list = list(rows)

with open(r'D:\Finish\dataset\y.csv', newline='') as file:
    # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
    #rows = csv.DictReader(csvfile) #csv.DictReader可以資料查找 d = {key1: value1, key2: value2}
    rows = csv.reader(file)
    data_list_y = list(rows)

print("list insert to array...")
for a in range(len(data_list)):
    x.append(data_list[a])
x=np.array(x)

for a in range(len(data_list_y)):
    y.append(data_list_y[a])


print("create train.csv...")
file = open('D:/p_test/train/no_9.csv',mode='w', newline='')
writer = csv.writer(file)
headers = ['label']

for b in range(13):
    for c in range(13):
        headers.append(str(b+1)+'x'+str(c+1))

writer.writerow(headers)

print("start convert to 2D-array...")
for b in range(len(x)):
    for c in range(15):
        if c == 9 or c == 10:
            x[b,c]=float(x[b,c])
        else:
            x[b,c]=int(float(x[b,c]))

for i in range(len(x)):
    for j in range(15):
        if j==0:
            size[j, int(x[i,j])] = 1#0~12 依序填1，填0會等於沒有
            continue
        if j >= 1 and j <=7 : #放撲克編碼
            if int(x[i,j])==-1:
                size[j] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            else:
                rank=int(x[i,j]) // 4 #牌號
                suit=int(x[i,j])%4+1 #花色 0~3 -> 1~4 填0會等於沒有
                size[j,rank] = suit
            continue
        if j==8: #hand_level讓每個格子都用到
            if int(x[i,j])==1:
                size[j, int(x[i,j])] = 1
            elif int(x[i,j])==2:
                size[j, 1] = 1
                size[j, 2] = 1
            elif int(x[i,j])==3:
                size[j, 2] = 1
                size[j, 3] = 1
                size[j, 4] = 1
            elif int(x[i,j])==4:
                size[j, 5] = 1
                size[j, 6] = 1
                size[j, 7] = 1
                size[j, 8] = 1
            elif int(x[i,j])==5:
                size[j, 8] = 1
                size[j, 9] = 1
                size[j, 10] = 1
                size[j, 11] = 1
                size[j, 12] = 1
            continue
        if j==9:#小數籌碼
            if int(float(x[i,j]))==0:
                size[j] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            else:
                if float(x[i,j])<=1:
                    size[j, 0] = 1
                elif float(x[i,j])<17:
                    size[j, 1] = 1
                elif float(x[i,j])<30:
                    size[j, 2] = 1
                elif float(x[i,j])<45:
                    size[j, 3] = 1
                elif float(x[i,j])<57:
                    size[j, 4] = 1
                elif float(x[i,j])<80:
                    size[j, 5] = 1
                elif float(x[i,j])<125:
                    size[j, 6] = 1
                elif float(x[i,j])<200:
                    size[j, 7] = 1
                elif float(x[i,j])<225:
                    size[j, 8] = 1
                elif float(x[i,j])<290:
                    size[j, 9] = 1
                elif float(x[i,j])<400:
                    size[j, 10] = 1
                elif float(x[i,j])<650:
                    size[j, 11] = 1
                else:
                    size[j, 12] = 1
            continue
        if j==10: #小數籌碼
            if int(float(x[i,j]))==-1:
                size[j] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            else:
                if float(x[i,j])<=1:
                    size[j, 0] = 1
                elif float(x[i,j])<17:
                    size[j, 1] = 1
                elif float(x[i,j])<30:
                    size[j, 2] = 1
                elif float(x[i,j])<45:
                    size[j, 3] = 1
                elif float(x[i,j])<57:
                    size[j, 4] = 1
                elif float(x[i,j])<80:
                    size[j, 5] = 1
                elif float(x[i,j])<125:
                    size[j, 6] = 1
                elif float(x[i,j])<200:
                    size[j, 7] = 1
                elif float(x[i,j])<225:
                    size[j, 8] = 1
                elif float(x[i,j])<290:
                    size[j, 9] = 1
                elif float(x[i,j])<400:
                    size[j, 10] = 1
                elif float(x[i,j])<650:
                    size[j, 11] = 1
                else:
                    size[j, 12] = 1
            continue
        if j>=11 and j<=14:
            if int(x[i, 11])==0 and int(x[i, 12])==1 and int(x[i, 13])==1 and int(x[i, 14])==0:
                size[11, 0:4] = [1,1,1,1]
            elif int(x[i, 11])==-1 and int(x[i, 12])==-1 and int(x[i, 13])==-1 and int(x[i, 14])==-1:
                size[11, 4:8] = [1,1,1,1]
            elif int(x[i, 11])==0 and int(x[i, 12])==0 and int(x[i, 13])==1 and int(x[i, 14])==1:
                size[11, 8:12] = [1,1,1,1]
            else:
                size[11] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            continue

    for k in range(13):
        all.append(size[k,])
        rrow.extend(size[k,])

    size = np.array([[0]*13]*13) #二維資料
    yy = [int(n) for n in y[i]]
    #將2 3 4 8 9 5轉1 2 3 4 5
    if yy[0]==2:
        yy[0]=0
    elif yy[0]==3:
        yy[0]=1
    elif yy[0]==4:
        yy[0]=2
    elif yy[0]==8:
        yy[0]=4
    elif yy[0]==9:
        yy[0]=3

    rrow.insert(0, yy[0])
    writer.writerow(rrow)
    rrow=[]

file.close()

all = np.array(all)
all = all.reshape(len(x),1,13,13)
print('维数：',all.shape)
print(all[0])
