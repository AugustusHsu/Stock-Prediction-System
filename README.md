# 股票預測系統
用歷史股票資料當作input建立簡單的LSTM預測模型來預測股票
## 抓股票程式
crawl_stock.py|內容
---|---
clean_row(row)|清除抓到的股票每個欄位中多餘的逗號還有空白
record(stock_id, row)|紀錄stock_id這隻股票的資料以append的方式增加在stock_id.csv後面
Initialize(Stock_ID)|初始化csv檔的column
Get_TSEdata(Day, Stock_ID)|爬Stock_ID這支股票指定日期Day這天的資料
Get_Stock_DATA(<br/>Stock_ID = ["2330"], <br/>First_Day = datetime.today(), <br/>Last_Day = datetime(2004,2,11))|抓取Stock_ID在日期範圍(First_Day,Last_Day)內的所有資料<br/>['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']<br/>預設抓台積電(2330)從今天到2004,2,11的資料

## 圖表化資料
graphical.py|內容
---|---
Graphical_Stock_DATA(PNGname,y)|圖表化的png名稱、要圖表化的資料
