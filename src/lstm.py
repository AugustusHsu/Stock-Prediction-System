'''
參考https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction
'''
## -*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import os
import time
import warnings
import numpy as np
import pandas as pd
from numpy import newaxis

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") #Hide messy Numpy warnings

#讀檔
def LoadData(Filename, ColumnList, WindowSize, NumOfPredictDay):
    #Filename = "../data/2002.csv"
    #ColumnList = ["成交股數","成交金額","成交筆數","開盤價","最後揭示買價","最後揭示賣價","收盤價"]
    #ColumnList = ["成交股數","成交金額","成交筆數","漲跌價差","最後揭示買價","最後揭示賣價","收盤價"]
    #WindowSize = 50
    #NumOfPredictDay = 1|7|10|30
    
    #用pandas讀檔
    df = pd.read_csv("../data/" + Filename)
    data = df.loc[:,ColumnList]
    
    #找非數字的欄位'--' 替換成 0
    for datashape_0 in range(data.shape[0]):
        for datashape_1 in range(data.shape[1]):
            if data.iloc[datashape_0,datashape_1] == '--':
                data.iloc[datashape_0,datashape_1] = 0
    
    #切割一筆一筆資料：TrainSet,TestSet的天數:WindowSize,NumOfPredictDay
    sequence_length = WindowSize + NumOfPredictDay
    #print(len(data))
    
    temp = []
    #減掉TrainSet+TestSet的大小,預防超過
    for index in range(len(data) - sequence_length):
        temp.append(data.iloc[index:index + sequence_length,:])
        #print(data[index: index + sequence_length])
    result = []
    for index in range(len(temp)):
        result.append(np.array(temp[index]))
    result = np.array(result)
    result = np.float32(result)
    return result

#正規化
def NormaliseWindows(DataSet):
    #複製DataSet
    result = np.array(DataSet, copy=True)
    for resultshape_0 in range(result.shape[0]):
        for resultshape_2 in range(result.shape[2]):
            base = float(result[resultshape_0 : resultshape_0 + 1, :1 , resultshape_2 : resultshape_2 + 1])
            if base != 0:
                for resultshape_1 in range(result.shape[1]):
                    vala = float(result[resultshape_0 : resultshape_0 + 1, resultshape_1 : resultshape_1 + 1, resultshape_2 : resultshape_2 + 1])
                    #print(vala)
                    result[resultshape_0 : resultshape_0 + 1, resultshape_1 : resultshape_1 + 1, resultshape_2 : resultshape_2 + 1] = vala / base - 1
    return result

#預設切割資料集方法(9:1的訓練資料集跟測試資料集)
def SplitData(DataSet, ColumnList, NumOfPredictDay):
    #複製DataSet
    result = np.array(DataSet, copy=True)
    #分割9:1的訓練資料集跟測試資料集
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    #前seq_len＋1當作input(x)
    #最後一個當作output(y)
    x_train = train[:, :-1*NumOfPredictDay]
    y_train = train[:, -1*NumOfPredictDay:,len(ColumnList)-1:len(ColumnList)]
    x_test = result[int(row):, :-1*NumOfPredictDay]
    y_test = result[int(row):, -1*NumOfPredictDay:,len(ColumnList)-1:len(ColumnList)]
    
    y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1]))
    y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1]))  
    
    return [x_train, y_train, x_test, y_test]

#切割資料集去做訓練
def SplitDatatoTrain(DataSet, ColumnList, NumOfPredictDay):
    #複製DataSet
    result = np.array(DataSet, copy=True)
    #訓練資料集
    train = result[:]
    #shuffle訓練資料
    np.random.shuffle(train)
    #前seq_len＋1當作input(x)
    #最後一個當作output(y)
    x_train = train[:, :-1*NumOfPredictDay]
    y_train = train[:, -1*NumOfPredictDay:,len(ColumnList)-1:len(ColumnList)]
    
    y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1]))
    print(x_train.shape)
    print(y_train.shape)
    
    return [x_train, y_train]

#切割資料集去預測
def SplitDatatoPredict(DataSet, ColumnList, NumOfPredictDay):
    #複製DataSet
    result = np.array(DataSet, copy=True)
    #預測資料
    predict = result[len(result)-1]
    #切割最後WindowSize天
    x_test = predict[NumOfPredictDay:]
    
    x_test = np.reshape(x_test, (1, x_test.shape[0], x_test.shape[1]))
    print(x_test.shape)
    
    return x_test

#切割資料集去測試
def SplitDatatoTest(DataSet, ColumnList, NumOfPredictDay):
    #複製DataSet
    result = np.array(DataSet, copy=True)
    #訓練資料集
    train = result[:len(result)-1]
    #預測資料
    predict = result[len(result)-1]
    #分割訓練資料集跟測試資料集
    np.random.shuffle(train)
    #前seq_len＋1當作input(x)
    #最後一個當作output(y)
    x_train = train[:, :-1*NumOfPredictDay]
    y_train = train[:, -1*NumOfPredictDay:,len(ColumnList)-1:len(ColumnList)]
    x_test = predict[:-1*NumOfPredictDay]
    y_test = predict[-1*NumOfPredictDay:,len(ColumnList)-1:len(ColumnList)]
    
    x_test = np.reshape(x_test, (1, x_test.shape[0], x_test.shape[1]))
    y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1]))
    y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1]))
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    
    return [x_train, y_train, x_test, y_test]

from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
#建立訓練模型
def build_model(Layer, Loss = "mse", Optimizer = "adam"):
    #Layer = [len(ColumnList), 50, 100,NumOfPredictDay]
    #Loss = "mse"
    #Optimizer = "adam"
    model = Sequential()
    
    model.add(LSTM( input_dim = Layer[0],
                    output_dim = Layer[1],
                    return_sequences = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(Layer[2], return_sequences = False))
    model.add(Dropout(0.2))
    
    model.add(Dense(output_dim = Layer[3]))
    model.add(Activation("linear"))
    
    start = time.time()
    model.compile(loss=Loss, optimizer=Optimizer)
    print("> Compilation Time : ", time.time() - start)
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted

import matplotlib.pyplot as plt
def plot_predict(predicted_data, NumOfPredictDay, true_data1, true_data2 = []):
    #reshape true data
    true_data1 = np.reshape(true_data1, (true_data1.shape[1], true_data1.shape[2]))
    true_data1 = true_data1[:,-1:]
    #plt true_data
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    #改true_data2
    padding = [None for p in range(NumOfPredictDay - len(true_data2))]
    ax.plot(list(true_data1) + list(true_data2) + padding, label='True Data')
    #plt predicted_data
    padding = [None for p in range(len(true_data1)-1)]
    plt.plot(padding + list(true_data1[-1]) + list(predicted_data), label='Prediction')
    plt.legend()
    plt.show()
    plt.clf()