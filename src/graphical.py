#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import os
import pandas as pd 
import matplotlib.pyplot as plt

def Graphical_Stock_DATA(Stock_ID):
    if not os.path.isdir('../grp'):
        os.makedirs('../grp')
    filepath = "../data/" + Stock_ID + ".csv"
    print(filepath)
    df = pd.read_csv(filepath)
    y = df['收盤價']
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
    plt.title(Stock_ID) 
        # 在這個指令之前，都還在做畫圖的動作 
        # 這個指令算是 "秀圖" 
    #plt.show() 
        # 如果要存成圖形檔:
        # 把 pyplot.show() 換成下面這行:
    savefigpath = "../grp/" + Stock_ID + ".png"
    plt.savefig(savefigpath,dpi=300,format="png") 

Graphical_Stock_DATA("2330")