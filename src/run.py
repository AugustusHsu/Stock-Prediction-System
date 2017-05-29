"""
參考https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lstm
import time
import os
import matplotlib.pyplot as plt

def plot_results_multiple(predicted_data, true_data, prediction_len, graph_store_path, csv_name):
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

#建立各種預測模型的圖路徑
slash = '/'
graph_path = '../grp'
nw_path = ['normalise_window_list_False','normalise_window_list_True']
ws_path = ['window_size_50']
layer_path = ['layer_1_50_100_1']
bs_path = ['batch_size_512']
#
epoch_path = ['epoch_1','epoch_5','epoch_10','epoch_25','epoch_50']
vs_path = ['validation_split_5percent']
optimizers_path = ['optimizers_rmsprop']
loss_path = ['loss_mse']

graph_store_path = []

for normalise_window in nw_path:
    for window_size in ws_path:
        for layer in layer_path:
            for batch_size in bs_path:
                for epoch in epoch_path:
                    for validation_split in vs_path:
                        for optimizers in optimizers_path:
                            for loss in loss_path:
                                filepath = (graph_path + slash 
                                          + normalise_window + slash 
                                          + layer + slash 
                                          + batch_size + slash 
                                          + epoch + slash 
                                          + validation_split + slash 
                                          + optimizers + slash 
                                          + loss + slash)
                                graph_store_path.append(filepath)
                                if not os.path.isdir(filepath):
                                    os.makedirs(filepath)

if not os.path.isdir("../grp/compare"):
    os.makedirs("../grp/compare")
#針對各個變數去做訓練和預測
nw_list = [False,True]
ws_list = [50]
layer_list = [[1,50,100,1]]
bs_list = [512]
#
epoch_list = [1]
vs_list = [0.05]
optimizers_list = ['rmsprop']
loss_list = ['mse']

count = 0

for normalise_window in nw_list:
    for window_size in ws_list:
        for layer in layer_list:
            for batch_sizes in bs_list:
                for epoch in epoch_list:
                    for validation_split in vs_list:
                        for optimizers in optimizers_list:
                            for loss in loss_list:
                                global_start_time = time.time()
                                epochs  = epoch
                                #輸入長度為seq_len的陣列
                                #輸出1
                                seq_len = window_size
                                
                                print('> Loading data... ')
                                
                                data_path = '../data/'
                                csv_name = ['2002']
                                csv = '.csv'
                                for csv_data in csv_name:
                                    X_train, y_train, X_test, y_test = lstm.load_data(str(data_path + csv_data + csv), seq_len, normalise_window)
                                
                                    print('> Data Loaded. Compiling...')
                                    
                                    #建立模型
                                    
                                    #build_model(layers,loss_choose="mse",optimizer_choose="rmsprop")
                                    model = lstm.build_model(layer,loss,optimizers)
                                    
                                    #訓練
                                    model.fit(
                                        X_train,
                                        y_train,
                                        batch_size=batch_sizes,
                                        nb_epoch=epochs,
                                        validation_split=validation_split)
                                    
                                    #預測
                                    predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
                                    #predicted = lstm.predict_sequence_full(model, X_test, seq_len)
                                    #predicted = lstm.predict_point_by_point(model, X_test)        
                                    
                                    print('Training duration (s) : ', time.time() - global_start_time)
                                    
                                    print("----------------分割線----------------")
                                    print("normalise_window:" + str(normalise_window))
                                    print("window_size:" + str(window_size))
                                    print("layer:" + str(layer))
                                    print("batch_sizes:" + str(batch_sizes))
                                    print("epoch:" + str(epoch))
                                    print("validation_split:" + str(validation_split))
                                    print("optimizers:" + str(optimizers))
                                    print("loss:" + str(loss))
                                    print("csv_name:" + str(csv_data) + csv)
                                    print("----------------分割線----------------")
                                    
                                    plot_results_multiple(predictions, y_test, 50, ("../grp/compare/" + "normalise_window_" + str(normalise_window)), csv_data)
                                    
                                    print('Training duration (s) : ', time.time() - global_start_time)
                                    
                                    count += 1
    
