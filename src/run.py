"""
參考https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lstm
import time
import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_results_multiple(predicted_data, true_data, prediction_len, graph_store_path, csv_name):
    '''
    #存預測圖
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.title(str(graph_store_path) + str(csv_name))

    savefigpath = str(graph_store_path) + str(csv_name) + ".png"
    plt.savefig(savefigpath,dpi=500,format="png") 
    plt.clf()
    '''
    #印出預測圖
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.title(str(graph_store_path) + str(csv_name))
        
    plt.show()
    plt.clf()

if not os.path.isdir("../schema"):
    os.makedirs("../schema")
#針對各個變數去做訓練和預測
NormalizeWindowList = [False,True]
WindowSizeList = [50]
LayerList = [[1,50,100,1]]
BatchSizeList = [512]
#
EpochList = [1]
ValidationSplitList = [0.1]
OptimizersList = ['adam']
LossList = ['mse']

#建立Model Information的Schema
if not os.path.isdir("../schema"):
    os.makedirs("../schema")
    
SchemaColumn = ['Name','Description','Sample']
ModelInformationSchema = pd.DataFrame(columns=SchemaColumn,index=range(8))

SchemaName = ['NormalizeWindowList','WindowSizeList','LayerList','BatchSizeList',
               'EpochList','ValidationSplitList','OptimizersList','LossList']

SchemaDescription = ['是否正規化資料','每個window的大小','神經網路的層數','訓練時Batch的大小',
                   '訓練幾次','驗證集大小','優化器的選擇','Loss Function的選擇']

SchemaSample = ['False,True','50','[1,50,100,1]','512',
                '1','0.1','adam','mse']
SchemaSample2 = [NormalizeWindowList,WindowSizeList,LayerList,BatchSizeList,
                 EpochList,ValidationSplitList,OptimizersList,LossList]

for i in range(8):
    ModelInformationSchema.iloc[i,0] = SchemaName[i]
    ModelInformationSchema.iloc[i,1] = SchemaDescription[i]
    ModelInformationSchema.iloc[i,2] = SchemaSample[i]
    #print(SchemaName[i],SchemaDescription[i],SchemaSample2[i])
    
ModelInformationSchema.to_csv('../schema/ModelInformationSchema.csv')
ModelInformationSchema

#建立Model Information
if not os.path.isdir("../model"):
    os.makedirs("../model")
ModelInformationColumn = SchemaName
ModelInformationColumn.append('StoredModelName')

NumofIndex = len(NormalizeWindowList)*len(WindowSizeList)*len(LayerList)*len(BatchSizeList)*\
             len(EpochList)*len(ValidationSplitList)*len(OptimizersList)*len(LossList)

ModelInformation = pd.DataFrame(columns=ModelInformationColumn,index=range(NumofIndex))

count = 0

for NormalizeWindow in NormalizeWindowList:
    for WindowSize in WindowSizeList:
        for Layer in LayerList:
            for BatchSize in BatchSizeList:
                #
                for Epoch in EpochList:
                    for ValidationSplit in ValidationSplitList:
                        for Optimizers in OptimizersList:
                            for Loss in LossList:
                                ModelInformation.iloc[count,0] = NormalizeWindow
                                ModelInformation.iloc[count,1] = WindowSize
                                ModelInformation.iloc[count,2] = Layer
                                ModelInformation.iloc[count,3] = BatchSize
                                ModelInformation.iloc[count,4] = Epoch
                                ModelInformation.iloc[count,5] = ValidationSplit
                                ModelInformation.iloc[count,6] = Optimizers
                                ModelInformation.iloc[count,7] = Loss
                                ModelInformation.iloc[count,8] = count
                                ModelInformation.to_csv('../model/ModelInformation.csv')
                                ModelInformation
                                
                                global_start_time = time.time()
                                #輸入長度為seq_len的陣列
                                #輸出1
                                seq_len = WindowSize
                                
                                print('> Loading data... ')
                                
                                data_path = '../data/'
                                csv_name = ['2002']
                                csv = '.csv'
                                for csv_data in csv_name:
                                    X_train, y_train, X_test, y_test = lstm.load_data(str(data_path + csv_data + csv), seq_len, NormalizeWindow)
                                
                                    print('> Data Loaded. Compiling...')
                                    
                                    #建立模型
                                    
                                    #build_model(layers,loss_choose="mse",optimizer_choose="rmsprop")
                                    model = lstm.build_model(Layer,Loss,Optimizers)
                                    
                                    #訓練
                                    model.fit(
                                        X_train,
                                        y_train,
                                        batch_size=BatchSize,
                                        nb_epoch=Epoch,
                                        validation_split=ValidationSplit)
                                    
                                    #HDF5, pip3
                                    model.save('../model/'+str(count)+'.h5')
                                    
                                    #預測
                                    predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
                                    #predicted = lstm.predict_sequence_full(model, X_test, seq_len)
                                    #predicted = lstm.predict_point_by_point(model, X_test)        
                                    
                                    print('Training duration (s) : ', time.time() - global_start_time)
                                    
                                    print("----------------分割線----------------")
                                    print("normalise_window:" + str(NormalizeWindow))
                                    print("window_size:" + str(WindowSize))
                                    print("layer:" + str(Layer))
                                    print("batch_sizes:" + str(BatchSize))
                                    print("epoch:" + str(Epoch))
                                    print("validation_split:" + str(ValidationSplit))
                                    print("optimizers:" + str(Optimizers))
                                    print("loss:" + str(Loss))
                                    print("csv_name:" + str(csv_data) + csv)
                                    print("----------------分割線----------------")
                                    
                                    plot_results_multiple(predictions, y_test, 50, ("../grp/compare/" + "normalise_window_" + str(NormalizeWindow)), csv_data)
                                    
                                    print('Training duration (s) : ', time.time() - global_start_time)
                                    
                                    count += 1
    
