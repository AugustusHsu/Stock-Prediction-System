'''
參考https://github.com/jimhsu123456/tsec
'''
## -*- coding: utf-8 -*-
#-*- coding: cp950 -*-
import os
import re
import csv
import logging
import requests
from lxml import html
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
        csv_Columns = ['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']
        cw.writerow(csv_Columns)
        f.close()

#爬Stock_ID這支股票指定日期Day這天的資料
def Get_TSEdata(Day, Stock_ID):
    #設定要開始爬的日期轉成民國，再設定網頁中要輸入的選項
    Date_str = '{0}/{1:02d}/{2:02d}'.format(Day.year - 1911, Day.month, Day.day)
    #print(Date_str)
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
    payload = {
        'download': '',
        'qdate': Date_str,
        'selectType': 'ALL'
    }
    #print(payload)
    # Get html page and parse as tree
    page = requests.post(url, data=payload)
    for ID in Stock_ID:
        Initialize(ID)
    if not page.ok:
        logging.error("Can not get TSE data at {}".format(Date_str))
    else:
        # Parse page
        tree = html.fromstring(page.text)

        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')
            for ID in Stock_ID:
                if str(tds[0]).strip() == ID:
                    #print(2330)
                    sign = tr.xpath('td/font/text()')
                    sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''
    
                    row = [
                        Date_str, # 日期
                        str(tds[2]), # 成交股數
                        str(tds[4]), # 成交金額
                        str(tds[5]), # 開盤價
                        str(tds[6]), # 最高價
                        str(tds[7]), # 最低價
                        str(tds[8]), # 收盤價
                        str(sign + tds[9]), # 漲跌價差
                        str(tds[3]),  # 成交筆數  
                    ]
                    #print(row)
                    clean_row(row)
                    print(row)
                    record(tds[0], row)

'''
抓取Stock_ID在日期範圍(First_Day,Last_Day)內的所有資料
['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']
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
    prefix="../data"
    if not os.path.isdir(prefix):
        os.mkdir(prefix)
        
    #The First_Day and Last_Day
    Date_str = '{0}/{1:02d}/{2:02d}'.format(First_Day.year - 1911, First_Day.month, First_Day.day)
    print("Start on " + Date_str)
    Date_str = '{0}/{1:02d}/{2:02d}'.format(Last_Day.year - 1911, Last_Day.month, Last_Day.day)
    print("End of " + Date_str)
    
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

    
Stock_ID = ["2330","2002","3008"]
#Stock_ID = ["2332"]
#Get_Stock_DATA(Stock_ID,Last_Day = datetime.today() - timedelta(365))
Get_Stock_DATA(Stock_ID)

