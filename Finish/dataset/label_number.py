import numpy as np
import pandas as pd

dataset=pd.read_csv('D:/Finish/dataset/test_2d_train.csv')#文件读取
dataset = dataset.values#去掉標頭
#dataset=np.array(dataset)
s1=0
s2=0
s3=0
s4=0
s5=0
print(dataset[0,11:15])

for row in dataset:
    if row[0]==0:
        s1+=1
    elif row[0]==1:
        s2+=1
    elif row[0]==2:
        s3+=1
    elif row[0]==3:
        s4+=1
    elif row[0]==4:
        s5+=1

print(len(dataset))
print("label 0數量: ", s1)
print("label 1數量: ", s2)
print("label 2數量: ", s3)
print("label 3數量: ", s4)
print("label 4數量: ", s5)
