#-*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import CrawlStock

CrawlStock.DailyUpdate()

import lstm
import time
import keras
import numpy as np
import pandas as pd

ColumnList = ['成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數',]

global_start_time = time.time()
PredictInformation = pd.read_pickle("../predict/PredictInformation.pickle")

for i in range(len(PredictInformation)):
    forloop_start_time = time.time()
    #
    FileName = PredictInformation['FileName'][i]
    WindowSize = PredictInformation['WindowSize'][i]
    NumOfPredictDay = PredictInformation['NumOfPredictDay'][i]
    PredictCSVName = PredictInformation['PredictCSVName'][i]
    
    print('Predict the ' + str(i) + '.h5 model')
    
    #載入資料
    DataSet = lstm.LoadData(FileName, ColumnList, WindowSize, NumOfPredictDay)
    #正規化資料
    NormalizeData = lstm.NormaliseWindows(DataSet)
    #切割預測資料
    x_predict = lstm.SplitDatatoPredict(DataSet, ColumnList, NumOfPredictDay)
    original_value = x_predict[0][0][len(ColumnList) - 1]
    x_predict = lstm.NormaliseWindows(x_predict)
    
    model = keras.models.load_model("../model/" + str(i) + '.h5')
    
    predictions = lstm.predict_point_by_point(model, x_predict)

    #lstm.plot_predict(predictions, NumOfPredictDay, x_predict)
    
    x_predict = np.reshape(x_predict, (x_predict.shape[1], x_predict.shape[2]))
    x_predict = x_predict[:,-1:]

    StoreData = pd.DataFrame(columns=['Data'], index=range(len(predictions) + len(x_predict)))
    for i in range(len(StoreData)):
        if i < len(x_predict):
            StoreData.iloc[i] = x_predict[i]
        else:
            StoreData.iloc[i] = predictions[i - len(x_predict)]
            
    StoreData = StoreData.applymap(lambda x: (x + 1) * original_value)        
    StoreData.to_pickle('../predict/' + PredictCSVName[:-4] + '.pickle')
    StoreData.to_json('../json/' + PredictCSVName[:-4] + '.json')
    StoreData.to_csv('../predict/' + PredictCSVName)
    print('Predict duration (s) : ',time.time() - forloop_start_time)

print('Total predict duration (s) : ',time.time() - global_start_time)

import os

DataList = os.listdir('../data')
for CSV in DataList[0:-2]:
    CSVFile = pd.read_csv('../data/' + CSV)
    CSVFile.to_json('../json/' + CSV[:-4] + '.json')
