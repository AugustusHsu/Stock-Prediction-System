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
from dateutil.relativedelta import relativedelta
import requests
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
                       '收盤價','漲跌價差','成交筆數',]
        cw.writerow(csv_Columns)
        f.close()
#爬Stock_ID這支股票指定日期Day這個月的資料
def Get_TSEdata(Day, Stock_ID):
    Date_str = '{0}{1:02d}{2:02d}'.format(Day.year, Day.month, Day.day)
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY'
    query_params = {
        'date': Date_str,
        'response': 'json',
        'stockNo': Stock_ID,
    }
    # Get json data
    page = requests.get(url, params=query_params)
    
    if not page.ok:
        logging.error("Can not get TSE data {} at {}".format(Stock_ID,Date_str))
    else:
        # Parse page
        content = page.json()
        for attri in content:
            if attri == 'data':
                for data in content['data']:
                    if data[0][3] == '/':
                        year = int(data[0][0:3]) + 1911
                    month = data[0][4:6]
                    day = data[0][7:9]
                    Store_time = '{0}-{1}-{2}'.format(year, month, day)
                    row = [
                        Store_time, # 日期
                        data[1], # 成交股數
                        data[2], # 成交金額
                        data[3], # 開盤價
                        data[4], # 最高價
                        data[5], # 最低價
                        data[6], # 收盤價
                        data[7], # 漲跌價差
                        data[8], # 成交筆數
                    ]
                    #print(row)
                    clean_row(row)
                    #print(row)
                    record(Stock_ID, row)
'''
抓取Stock_ID在日期範圍(First_Day,Last_Day)內的所有資料
['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']
'''
#預設抓台積電(2330)從今天到1991,1,1的資料
def Get_Stock_DATA(Stock_ID = ["2330"], First_Day = datetime.today(), Last_Day = datetime(1992,1,1)):
    #Set Stock_ID that need to crawl
    print("Crawl " + str(Stock_ID) + " Stock Data")
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
        
    #當Stock_ID為空不執行
    if Stock_ID == []:
        print("Nothing to crawl")
        return
    #針對每個Stock_ID去做初始化有就略過沒有就做
    for ID in Stock_ID:
        Initialize(ID)
        #The First_Day and Last_Day
        ROC_Date_str = '{0}/{1:02d}/{2:02d}'.format(Last_Day.year - 1911, Last_Day.month, Last_Day.day)
        Date_str = '{0}/{1:02d}/{2:02d}'.format(Last_Day.year, Last_Day.month, Last_Day.day)
        print("Start on " + ROC_Date_str)
        print("Start on " + Date_str)
        ROC_Date_str = '{0}/{1:02d}/{2:02d}'.format(First_Day.year - 1911, First_Day.month, First_Day.day)
        Date_str = '{0}/{1:02d}/{2:02d}'.format(First_Day.year, First_Day.month, First_Day.day)
        print("End of " + ROC_Date_str)
        print("End of " + Date_str)

        #Set Max_Error to 5
        Max_Error = 5
        Error_Times = 0
        #Crawl stock until Last_Day
        while Error_Times < Max_Error and First_Day >= Last_Day:
            try:
                print('抓取{0} 第{1:02d}年{2:02d}月'.format(ID, Last_Day.year, Last_Day.month))
                Get_TSEdata(Last_Day, ID)
                time.sleep(0.1)
                Error_Times = 0
            except:
                '''When crawl data occuring problem add one to Error_Times'''
                date_str = Last_Day.strftime('%Y/%m/%d')
                logging.error('Crawl raise error {}'.format(date_str))
                Error_Times += 1
                continue
            finally:
                Last_Day += relativedelta(months=1)
        Last_Day = datetime(1992,1,1)
        print("Finish")
#爬Stock_ID這支股票指定日期Day這個月的資料
def Get_Stock_Data_by_Day(Day, Stock_ID):
    Date_str = '{0}{1:02d}{2:02d}'.format(Day.year, Day.month, Day.day)
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY'
    query_params = {
        'date': Date_str,
        'response': 'json',
        'stockNo': Stock_ID,
    }
    # Get json data
    page = requests.get(url, params=query_params)
    
    if not page.ok:
        logging.error("Can not get TSE data {} at {}".format(Stock_ID,Date_str))
    else:
        # Parse page
        content = page.json()
        for attri in content:
            if attri == 'data':
                for data in content['data']:
                    if data[0][3] == '/':
                        year = int(data[0][0:3]) + 1911
                    month = data[0][4:6]
                    day = data[0][7:9]
                    Date = datetime(year, int(month), int(day))
                    if Day == Date:
                        Store_time = '{0}-{1}-{2}'.format(year, month, day)
                        row = [
                            Store_time, # 日期
                            data[1], # 成交股數
                            data[2], # 成交金額
                            data[3], # 開盤價
                            data[4], # 最高價
                            data[5], # 最低價
                            data[6], # 收盤價
                            data[7], # 漲跌價差
                            data[8], # 成交筆數
                        ]
                        #print(row)
                        clean_row(row)
                        print(row)
                        record(Stock_ID, row)
#每日更新，去讀取資料夾內的StockID更新
def DailyUpdate():
    #找../data裡面有的股票資料去更新
    DataList = os.listdir("../data")
    print(DataList[0:-2])
    print("Update...")
    for CSV in DataList[0:-2]:
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
            
            for ID in Stock_ID:
                #最多Error 5次
                Max_Error = 5
                Error_Times = 0
                #Crawl stock until Last_Day
                while Error_Times < Max_Error and Today >= LastUpdate:
                    try:
                        print('抓取{0} 第{1:02d}年{2:02d}月{3:02d}日'.format(ID, LastUpdate.year, LastUpdate.month, LastUpdate.day))
                        Get_Stock_Data_by_Day(LastUpdate, ID)
                        time.sleep(0.1)
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
#DailyUpdate()
#Stock_ID = ["2330","2002","3008",'2332','12','123']
#CrawlID = CheckCSV(Stock_ID)