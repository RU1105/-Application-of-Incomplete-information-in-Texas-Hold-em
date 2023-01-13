import random
import numpy as np
import numpy as reshape
import csv

np.set_printoptions(threshold=np.inf)
d2=[]

print("reading file...")
with open(r'D:\Finish\dataset\2_test_2d_train.csv', newline='') as csvfile:
    # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
    #rows = csv.DictReader(csvfile) #csv.DictReader可以資料查找 d = {key1: value1, key2: value2}
    rows = csv.reader(csvfile)
    data_list = list(rows)

print("list insert to array...")
for a in range(len(data_list)):
    d2.append(data_list[a])
#d2=np.array(d2)

print("create train.csv...")
file = open('D:/Finish/dataset/3_test_2d_train.csv',mode='w', newline='')
writer = csv.writer(file)

new2=[]
new=[]

for a in d2:
    if a[0]=='2':
        new2.append(a)
    else:
        if a[0]!='4' and a[0]!='3':
            new.append(a)

b = random.sample(range(len(new2)), 200000)

for a in b:
    new.append(new2[a])


for a in range(len(new)):
    writer.writerow(new[a])
