"""
參考https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lstm
import time


global_start_time = time.time()
epochs  = 1
#輸入長度為seq_len的陣列
#輸出1
seq_len = 50

print('> Loading data... ')

X_train, y_train, X_test, y_test = lstm.load_data('sp500.csv', seq_len, True)

print('> Data Loaded. Compiling...')

#建立模型
#訓練
#預測

print('Training duration (s) : ', time.time() - global_start_time)