import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from scipy import stats
from threading import Thread
from io import BytesIO
import requests,json,random,os,base64


class tradelight:
    
    def __init__(self):
        pass
    
    def getCandles(self,symbol,interval,fromdate,enddate,dump=False):
        self.symbol,self.interval,self.fromdate,self.enddate = symbol,interval,fromdate,enddate
        url = "https://kitecharts.zerodha.com/api/chart"
        chart_public_token = "45cf7bf62171873fd35151ce19a65720"
        chart_api_key = "kitefront"
        chart_access_token = "V6CNXwEqpijuOzf6dYnAJMpaaJYRtHu6"
        user_id = "ZP2572"
        urlData = url+"/{}/{}?public_token={}&user_id={}&api_key={}&access_token={}&from={}&to={}".format(
                self.getSymbolToken(),
                interval,
                chart_public_token,
                user_id,
                chart_api_key,
                chart_access_token,
                fromdate,
                enddate)
        try:
            webURL = requests.get(urlData)
            if dump:
                fp = open("static/resources/dump/{}".format(symbol),"w")
                fp.write(webURL.text)
                fp.close()
            else:
                JSON_object = json.loads(webURL.text)
                self.resdata = JSON_object["data"]["candles"]
        except:
            pass
    
    def lastCandle(self,index):
        candle = self.resdata[-1]
        return(candle[index])
        
    def getCandleItems(self,index):
        item = []
        for candle in self.resdata:
            item.append(candle[index])
        return(item)
    
    def getChart(self,capital,quantity,short_mavg,long_mavg,dump=False):
        df = pd.DataFrame({"timestamp": self.getCandleItems(0),"close": self.getCandleItems(4)})
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp")
        
        df["short_mavg"] = df.close.rolling(window=short_mavg, min_periods=1, center=False).mean()
        df["long_mavg"] = df.close.rolling(window=long_mavg, min_periods=1, center=False).mean()
        df["signal"] = 0
        df["signal"][short_mavg:] = np.where(df.short_mavg[short_mavg:] > df.long_mavg[short_mavg:],1,0)
        df["signal"] = quantity * df.signal
        df["position"] = df.signal.diff()
        df["holdings"] = df.close.multiply(df.signal,axis=0)
        df["cash"] = capital - df.position.multiply(df.close,axis=0).cumsum()
        df["total"] = df.cash + df.holdings
        df["return"] = df.total.pct_change()
        
        income = df.total.values[-1]
        
        if dump:
            fp = open("static/resources/data/stockreturn.csv","a")
            fp.write("\n{},{},{},{},{},{},{}".format(self.symbol,capital,quantity,income,df.close.mean(),df.index[0],df.index[-1]))
            fp.close()
        else:
            fig = plt.figure(figsize=(8,4))
            ax = fig.add_subplot(111)
            df[["close","short_mavg","long_mavg"]].plot(ax=ax)
            ax.plot(df.loc[df.position == quantity].index,df.close[df.position == quantity],"^",color="g")
            ax.plot(df.loc[df.position == -quantity].index,df.close[df.position == -quantity],"v",color="r")

            figfile = BytesIO()
            plt.grid(True)
            plt.savefig(figfile, format='png', bbox_inches='tight')
            figfile.seek(0)
            figdata_png = (self.symbol,capital,quantity,income,base64.b64encode(figfile.getvalue()).decode('utf8'))
            return(figdata_png)
    
    def instruments(self):
        df = pd.read_csv("static/resources/data/instruments.csv")
        return(df)
    
    def getSymbolToken(self):
        df_instruments = self.instruments()
        symboltoken = df_instruments[df_instruments.tradingsymbol == self.symbol].instrument_token.values[0]
        return(symboltoken)
    
    def dumpInstrumentHistoricalData(self,interval,fromdate,enddate):
        idf = self.instruments()
        for symbol in idf.tradingsymbol.values:
            Thread(target=self.getCandles, args=(symbol,interval,fromdate,enddate,True)).start()
    
    def symbolsGetReturns(self,capital,quantity,short_mavg,long_mavg):
        fp = open("static/resources/data/stockreturn.csv","w")
        fp.write("symbol,capital,quantity,income,avg_close,start_date,end_date")
        fp.close()
        items = os.listdir("static/resources/dump")
        for symbol in items:
            self.getCandlesFromLocal(symbol)
            try:
                if len(self.resdata) > 20:
                    tolerance = self.thresold()
                    last_close = self.lastCandle(4)
                    if tolerance[0] > last_close:
                        self.getChart(capital,quantity,short_mavg,long_mavg,True)
            except:
                pass
    
    def getCandlesFromLocal(self,symbol):
        self.symbol = symbol
        try:
            fp = open("static/resources/dump/{}".format(symbol),"r")
            JSON_object = json.loads(fp.read())
            fp.close()
            self.resdata = JSON_object["data"]["candles"]
        except:
            pass
    
    def thresold(self):
        close = self.getCandleItems(4)
        mean = np.mean(close)
        std = np.std(close)
        if (mean > 0) & (std > 0):
            t = stats.norm.interval(0.95,mean,std)
            return(t)