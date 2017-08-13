#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import os
import pandas as pd 
import matplotlib.pyplot as plt
#圖表化的png名稱、要圖表化的資料
def Graphical_Stock_DATA(PNGname,y):
    if not os.path.isdir('../grp'):
        os.makedirs('../grp')
    x = range(len(y))
    # 開始畫圖
        # 設定要畫的的x,y數據list....
    plt.plot(x,y)
        # 設定圖的範圍, 不設的話，系統會自行決定
    #plt.xlim(-30,390)
    #plt.ylim(-1.5,1.5)
        # 照需要寫入x 軸和y軸的 label 以及title
    plt.xlabel("Day") 
    plt.ylabel("Stock price") 
    plt.title(PNGname) 
        # 在這個指令之前，都還在做畫圖的動作 
        # 這個指令算是 "秀圖" 
    #plt.show() 
        # 如果要存成圖形檔:
        # 把 pyplot.show() 換成下面這行:
    savefigpath = "../grp/" + PNGname + ".png"
    plt.savefig(savefigpath,dpi=1000,format="png") 
    plt.clf()

Stock_ID = ["2330","2002","3008"]
for ID in Stock_ID:
    filepath = "../data/" + ID + ".csv"
    print(filepath)
    df = pd.read_csv(filepath)
    y = df['收盤價'].iloc[:365]
    Graphical_Stock_DATA(ID,y)