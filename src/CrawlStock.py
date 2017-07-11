'''
參考https://github.com/Asoul/tsec
'''
## -*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import os
import re
import csv
import logging
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
'''
定義Fuction
'''

#清除抓到的股票每個欄位中多餘的逗號還有空白
def clean_row(row):
    ''' Clean comma and spaces '''
    for index, content in enumerate(row):
        row[index] = re.sub(",", "", content.strip())
    return row

#紀錄stock_id這隻股票的資料以append的方式增加在stock_id.csv後面
def record(stock_id, row):
    ''' Save row to csv file '''
    prefix="data"
    f = open('../{}/{}.csv'.format(prefix, stock_id.strip()), 'a')
    cw = csv.writer(f, lineterminator='\n')
    cw.writerow(row)
    f.close()
    
#初始化csv檔的column
def Initialize(Stock_ID):
    #初始化Stock_ID.csv
    prefix = "../data"
    if not os.path.isfile('{}/{}.csv'.format(prefix, Stock_ID.strip())):
        ''' Save row to csv file '''
        f = open('{}/{}.csv'.format(prefix, Stock_ID.strip()), 'a', encoding='utf-8-sig')
        cw = csv.writer(f, lineterminator='\n')
        csv_Columns = ['日期','成交股數','成交金額','開盤價','最高價','最低價',
                       '收盤價','漲跌價差','成交筆數','最後揭示買價','最後揭示賣價',]
        cw.writerow(csv_Columns)
        f.close()
        
#爬Stock_ID這支股票指定日期Day這天的資料
def Get_TSEdata(Day, Stock_ID):
    #設定網頁中要輸入的選項，再設定要儲存的日期格式
    Date_str = '{0}{1:02d}{2:02d}'.format(Day.year, Day.month, Day.day)
    Store_time = '{0}-{1:02d}-{2:02d}'.format(Day.year, Day.month, Day.day)
    #print(Date_str)
    url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'
    query_params = {
        'date': Date_str,
        'response': 'json',
        'type': 'ALL',
        '_': str(round(time.time() * 1000) - 500)
    }
    # Get json data
    page = requests.get(url, params=query_params)
    for ID in Stock_ID:
        Initialize(ID)
    if not page.ok:
        logging.error("Can not get TSE data at {}".format(Date_str))
    else:
        # Parse page
        content = page.json()
        #print(content)
        for attri in content:
            #print(attri)
            if attri == 'data5' or attri == 'data4' or attri == 'data3' or  attri == 'data2' or attri == 'data1':
                for data in content[attri]:
                    for ID in Stock_ID:
                        if str(data[0]).strip() == ID:
                            sign = '-' if data[9].find('green') > 0 else ''
                            #print(data)
                            row = [
                                Store_time, # 日期
                                data[2], # 成交股數
                                data[4], # 成交金額
                                data[5], # 開盤價
                                data[6], # 最高價
                                data[7], # 最低價
                                data[8], # 收盤價
                                sign + data[10], # 漲跌價差
                                data[3], # 成交筆數
                                data[11],#最後揭示買價
                                data[13],#最後揭示賣價
                            ]
                            #print(row)
                            clean_row(row)
                            print(row)
                            record(data[0], row)

'''
抓取Stock_ID在日期範圍(First_Day,Last_Day)內的所有資料
['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數','最後揭示買價','最後揭示賣價']
'''
#預設抓台積電(2330)從今天到2004,2,11的資料
def Get_Stock_DATA(Stock_ID = ["2330"], First_Day = datetime.today(), Last_Day = datetime(2004,2,11)):
    #Set Stock_ID that need to crawl
    print("Crawl " + str(Stock_ID) + "Stock Data")
    #Set logging
    if not os.path.isdir('../log'):
        os.makedirs('../log')
    logging.basicConfig(filename='../log/crawl-error.log',
                        level=logging.ERROR,
                        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')
    #Make directory if not exist when initialize
    prefix='../data'
    if not os.path.isdir(prefix):
        os.mkdir(prefix)
        
    #The First_Day and Last_Day
    Date_str = '{0}/{1:02d}/{2:02d}'.format(First_Day.year - 1911, First_Day.month, First_Day.day)
    CE_Date_str = '{0}/{1:02d}/{2:02d}'.format(First_Day.year, First_Day.month, First_Day.day)
    print("Start on " + Date_str)
    print("Start on " + CE_Date_str)
    Date_str = '{0}/{1:02d}/{2:02d}'.format(Last_Day.year - 1911, Last_Day.month, Last_Day.day)
    CE_Date_str = '{0}/{1:02d}/{2:02d}'.format(Last_Day.year, Last_Day.month, Last_Day.day)
    print("End of " + Date_str)
    print("End of " + CE_Date_str)
    
    #Set Max_Error to 5
    Max_Error = 5
    Error_Times = 0
    #Crawl stock until Last_Day
    while Error_Times < Max_Error and First_Day >= Last_Day:
        try:
            Get_TSEdata(Last_Day, Stock_ID)
            Error_Times = 0
        except:
            '''When crawl data occuring problem add one to Error_Times'''
            date_str = Last_Day.strftime('%Y/%m/%d')
            logging.error('Crawl raise error {}'.format(date_str))
            Error_Times += 1
            continue
        finally:
            Last_Day += timedelta(1)
            
    print("Finish")

#每日更新，去讀取資料夾內的StockID更新
def DailyUpdate():
    #找../data裡面有的股票資料去更新
    DataList = os.listdir("../data")
    print(DataList[2:])
    print("Update...")
    for CSV in DataList[2:]:
        #讀檔去找最後一筆的日期
        print("{}".format(CSV[:-4]))
        df = pd.read_csv("../data/{}.csv".format(CSV[:-4]))
        date = np.array(df.iloc[df.shape[0]-1:df.shape[0],:1])

        strdate = str(date)
        #最後一筆的日期
        year = int(strdate[3:7])
        month = int(strdate[8:10])
        day = int(strdate[11:13])
        Stock_ID = []
        Stock_ID.append(CSV[:-4])
        
        LastUpdate = datetime(year,month,day) + timedelta(1)
        Today = datetime.today()
        if LastUpdate != Today:
            LastUpdate_str = '{0}/{1:02d}/{2:02d}'.format(LastUpdate.year, LastUpdate.month, LastUpdate.day)
            Today_str = '{0}/{1:02d}/{2:02d}'.format(Today.year, Today.month, Today.day)
            print("From {} to {} (Today)".format(LastUpdate_str, Today_str))
            
            #最多Error 5次
            Max_Error = 5
            Error_Times = 0
            #Crawl stock until Last_Day
            while Error_Times < Max_Error and Today >= LastUpdate:
                try:
                    Get_TSEdata(LastUpdate, Stock_ID)
                    Error_Times = 0
                except:
                    #When crawl data occuring problem add one to Error_Times
                    date_str = LastUpdate.strftime('%Y/%m/%d')
                    logging.error('Crawl raise error {}'.format(date_str))
                    Error_Times += 1
                    continue
                finally:
                    LastUpdate += timedelta(1)
        else:
            print("Nothing to Update")

#回傳資料夾data內沒有的Stock_ID，可以藉由這個抓取沒在資料庫內的股票
def CheckCSV(Stock_ID):
    prefix = "../data"
    CrawlID = []
    for ID in Stock_ID:
        if not os.path.isfile('{}/{}.csv'.format(prefix, ID.strip())):
            CrawlID.append(ID)
    #Get_Stock_DATA(CrawlID)
    return CrawlID


#Stock_ID = ["2330","2002","3008",'2332']
#Stock_ID = ["2332"]
#datetime(2004,2,11) data2
#datetime(2009,1,5) data4
#datetime(2011,8,1) data5
#Get_Stock_DATA(Stock_ID, Last_Day = datetime.today() - timedelta(10))
#Get_Stock_DATA(Stock_ID=Stock_ID)
#Get_TSEdata(datetime(2009,1,5), ['3008'])
DailyUpdate()
Stock_ID = ["2330","2002","3008",'2332','12','123']
CrawlID = CheckCSV(Stock_ID)