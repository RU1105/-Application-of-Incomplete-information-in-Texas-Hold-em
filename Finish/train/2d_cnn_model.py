import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers
# 用來後續將 label 標籤轉為 one-hot-encoding
from keras.utils import np_utils
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from itertools import product 
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import EarlyStopping

dataset=[]
dataset=np.array(dataset)

dataset=pd.read_csv('D:/Finish/dataset/2_test_2d_train.csv')#文件读取71500
dataset = dataset.values#去掉標頭

#train.csv第一列为数字类别标签，后面所有列均为像素值，故一共785列（784+1）
data = np.array(dataset[:,1:170]) #从第二列开始读取为训练数据
label = np.array(dataset[:,0:1]) #读取第一列为数字类别标签
data = np.reshape(data, (-1,13,13,1)) #更改为网络输入类型，即原始图像shape（28*28*1）
#data, label = shuffle(data, label, random_state=0) #打亂數據集

#分训练集和測試集8:2
train_data,test_data,train_label,test_label = train_test_split(data,label,test_size=0.2, train_size=0.8, random_state=2, stratify=label, shuffle=True) #要改7:2:1 ,line 88, 混淆矩陣
#分測試集和驗證集1:1
test_data, val_data, test_label, val_label = train_test_split(test_data, test_label, test_size=0.5, train_size=0.5, random_state=2, stratify=test_label, shuffle=True)

"""#看label有沒有平均分配
s1=0
s2=0
s3=0

for a in range(len(train_label)):
    if train_label[a]==[3]:
        s1+=1

for a in range(len(test_label)):
    if test_label[a]==[3]:
        s2+=1

for a in range(len(val_label)):
    if val_label[a]==[3]:
        s3+=1

t=s1+s2+s3
print("train: {:2.1f}%".format((s1/t)*100.0))
print("test: {:2.1f}%".format((s2/t)*100.0))
print("val: {:2.1f}%".format((s3/t)*100.0))
print("total label 3: ", t)

#檢查資料集有無出錯
print(train_data[0])
print(train_label[0])"""


#分训练集和验证集
#train_label=tf.squeeze(train_label)
#test_label=tf.squeeze(test_label)
# 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 array([0., 0., 0., 0., 0., 0., 0., 1., 0., 0.], dtype=float32)，即第7個值為 1
train_label_onehot = np_utils.to_categorical(train_label, 3)
test_label_onehot = np_utils.to_categorical(test_label, 3)
val_label_onehot = np_utils.to_categorical(val_label, 3)

# 將 training 的 input 資料轉為 28*28 的 2維陣列
# training 與 testing 資料數量分別是 60000 與 10000 筆
# train_data_2D 是 [60000, 28*28] 的 2維陣列
# 轉換色彩 0~255 資料為 0~1
train_data_2D = train_data.astype('float32')
test_data_2D = test_data.astype('float32')
val_data_2D = val_data.astype('float32')

"""train_data_norm = train_data_2D
test_data_norm = test_data_2D
val_data_norm = val_data_2D"""

# 建立簡單的線性執行的模型，調參數，
model = Sequential()
#參考AlexNet
model.add(Conv2D(filters=96, kernel_size=(11, 11), strides=4,  padding='same', input_shape=(13, 13, 1), activation='relu'))

model.add(Conv2D(filters=256, kernel_size=(5, 5), strides=1, padding='same', activation='relu'))

model.add(Conv2D(filters=384, kernel_size=(3, 3), strides=1, padding='same', activation='relu'))
model.add(Conv2D(filters=384, kernel_size=(3, 3), strides=1, padding='same', activation='relu'))

model.add(Conv2D(filters=256, kernel_size=(3, 3), strides=1, padding='same', activation='relu'))


#model.add(MaxPooling2D(pool_size=(3, 3), strides=2, padding='same'))
#model.add(Dropout(0.5))

# 不用池化層，因為flop0~flop4 hand0~hand1的位置代表手牌牌值的大小
model.add(Flatten())
#kernel_regularizer=regularizers.l1(0.5),activity_regularizer=regularizers.l1_l2(0.5) ), bias_regularizer=regularizers.l2(0.05)
model.add(Dense(2048, activation='relu'))
#model.add(Dropout(0.5))

model.add(Dense(2048, activation='relu'))
model.add(Dense(3, activation='softmax'))

# 打印模型结构
model.summary()
#warn up

# 編譯: 選擇損失函數、優化方法及成效衡量方式 tf.keras.optimizers.SGD(LR)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#EarlyStop=EarlyStopping(monitor='val_accuracy', patience=2,verbose=1, mode='auto')
Reduce=ReduceLROnPlateau(monitor='val_accuracy',factor=0.1,patience=1,verbose=1,mode='auto',min_delta=0.000001,cooldown=0,min_lr=0)


# 進行 model 訓練, 訓練過程會存在 train_history 變數中
# 將 60000 張 training set 的圖片，用 80% (48000張) 訓練模型，用 20% (12000張) 驗證結果
# epochs 10 次，就是訓練做了 10 次
# batch_size 是 number of samples per gradient update，每一次進行 gradient descent 使用幾個 samples
# verbose 是 train_history 的 log 顯示模式，2 表示每一輪訓練，列印一行 log
# validation_data验证集 , validation_data=(test_data_2D, test_label_onehot), callbacks=[callback]
train_history = model.fit(x=train_data_2D, y=train_label_onehot, validation_data=(val_data_2D, val_label_onehot), callbacks=[Reduce], epochs=100, batch_size=128, verbose=2)

# 用 10000 筆測試資料，評估訓練後 model 的成果(分數)
scores = model.evaluate(test_data_2D, test_label_onehot)
print()
print("Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))

"""# 預測(prediction)
X = test_data_2D[0:10,:]
predictions = model.predict(X)
# get prediction result
Final_prediction = [result.argmax() for result in predictions][0]
#predict = np.argmax(predictions,1)
print("predict: ",Final_prediction)"""


# 模型訓練結果 結構存檔
from keras.models import model_from_json
json_string = model.to_json()
with open("D:/Finish/train/model.config", "w") as text_file:
    text_file.write(json_string)

# 模型訓練結果 權重存檔
model.save_weights("D:/Finish/train/model.weight")

#顯示train與test dataset訓練過程的誤差率。
plt.clf()

plt.plot(train_history.history['loss'])
plt.plot(train_history.history['val_loss'])
plt.title('Train History')
plt.ylabel('loss')
plt.xlabel('Epoch')
plt.legend(['loss', 'val_loss'], loc='upper left')
#plt.show()
plt.savefig('D:/Finish/train/loss.png')

#顯示train與test dataset訓練過程的準確率。
plt.clf()
plt.plot(train_history.history['accuracy'])
plt.plot(train_history.history['val_accuracy'])
plt.title('Train History')
plt.ylabel('accuracy')
plt.xlabel('Epoch')
plt.legend(['accuracy', 'val_accuracy'], loc='upper left')
#plt.show()
plt.savefig('D:/Finish/train/accuracy.png')


def plot_confusion_matrix(cm,classes,title='Confusion matrix'):
    cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
    plt.imshow(cm,interpolation='nearest',cmap='Blues')
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks,rotation=45)
    plt.yticks(tick_marks,classes)
    thresh = cm.max() / 2.
    for i,j in product(range(cm.shape[0]),range(cm.shape[1])):
        plt.text(j,i,'{:.2f}'.format(cm[i,j]),horizontalalignment="center",color="white" if cm[i,j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('D:/Finish/train/matrix.png')
    plt.show()

# 顯示混淆矩陣
def plot_confuse(model,x_val,y_val):
    predictions = model.predict(x_val).argmax(axis=1) #是找陣列中預測值最大的label
    truelabel = y_val.argmax(axis=-1).astype('float32') # 將one-hot轉化為label，再轉成float
    conf_mat = confusion_matrix(y_true=truelabel,y_pred=predictions) #predictions, truelabel要一樣的type，要不然會錯
    plt.figure()
    plot_confusion_matrix(conf_mat,range(np.max(truelabel.astype(int))+1)) #truelabel要轉回int

print(val_data.shape)	# (25838, 48, 48, 1)
print(val_label_onehot.shape)	# (25838, 7)
plot_confuse(model, val_data, val_label_onehot)
