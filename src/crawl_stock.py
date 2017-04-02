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
def clean_row(row):
    ''' Clean comma and spaces '''
    for index, content in enumerate(row):
        row[index] = re.sub(",", "", content.strip())
    return row

def record(stock_id, row):
    ''' Save row to csv file '''
    prefix="data"
    f = open('../{}/{}.csv'.format(prefix, stock_id), 'a')
    cw = csv.writer(f, lineterminator='\n')
    cw.writerow(row)
    f.close()
def Get_TSEdata(Day, Stock_ID):
    '''Make payload to search the stock priece on the website'''
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
抓台積電(2330)從今天到2004,2,11的資料
'''
'''Set logging'''
if not os.path.isdir('../log'):
    os.makedirs('../log')
logging.basicConfig(filename='../log/crawl-error.log',
    level=logging.ERROR,
    format='%(asctime)s\t[%(levelname)s]\t%(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
''' Make directory if not exist when initialize '''
prefix="../data"
if not os.path.isdir(prefix):
    os.mkdir(prefix)
    
    
    
'''Set the First_Day and Last_Day '''
First_Day = datetime.today()
Last_Day = datetime(2004, 2, 11)
print(First_Day)
print(Last_Day)
'''Set Stock_ID that need to crawl'''
Stock_ID = ["2330"]
print(Stock_ID)


'''Set Max_Error to 5'''
Max_Error = 5
Error_Times = 0
'''Crawl stock until Last_Day'''
while Error_Times < Max_Error and First_Day >= Last_Day:
    try:
        Get_TSEdata(First_Day, Stock_ID)
        Error_Times = 0
    except:
        '''When crawl data occuring problem add one to Error_Times'''
        date_str = First_Day.strftime('%Y/%m/%d')
        logging.error('Crawl raise error {}'.format(date_str))
        Error_Times += 1
        continue
    finally:
        First_Day -= timedelta(1)
        
print("Finish")