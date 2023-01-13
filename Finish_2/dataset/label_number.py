import numpy as np
import pandas as pd

dataset=pd.read_csv('D:/porker_cnn/完成/y.csv')#文件读取
dataset = dataset.values#去掉標頭
#dataset=np.array(dataset)
s1=0
s2=0
s3=0
s4=0
s5=0
print(dataset[0])

for row in dataset:
    if row[0]==2:
        s1+=1
    elif row[0]==3:
        s2+=1
    elif row[0]==4:
        s3+=1
    elif row[0]==8:
        s4+=1
    elif row[0]==9:
        s5+=1

print("label 0(Raise)數量 : ", s1)
print("label 1(Call)數量  : ", s2)
print("label 2(Check)數量 : ", s3)
print("label 3(Fold)數量  : ", s4)
print("label 4(All-in)數量: ", s5)
print("Total label數量    : ",len(dataset))

print()
print("label 0(Raise)占比 : {:.1f}%".format(s1/len(dataset)*100))
print("label 1(Call)占比  : {:.1f}%".format(s2/len(dataset)*100))
print("label 2(Check)占比 : {:.1f}%".format(s3/len(dataset)*100))
print("label 3(Fold)占比  : {:.1f}%".format(s4/len(dataset)*100))
print("label 4(All-in)占比: {:.1f}%".format(s5/len(dataset)*100))
