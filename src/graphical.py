#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:45:44 2017

@author: jim
"""
import pandas as pd 
df = pd.DataFrame
df.columns = ['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']
df = pd.read_csv("../data/2330.csv")

print(df)

print(df.columns)