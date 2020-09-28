from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.exceptions import V20Error

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplfinance as mpf

def main():
    access_token = "df36fd83bc0d3b33010ebbea7feb99d7-5849f313292879ab44e0a824de58e1ad"
    api = API(access_token=access_token, environment="practice")
    # count = 2000
    count = 100

    params = {
        "count": count,  # 足3本取得
        "granularity": "M5",  # 1分足を取得
        "price": "B",  # Bidを取得
    }
    instruments_candles = instruments.InstrumentsCandles(instrument="GBP_USD", params=params)

    try:
        api.request(instruments_candles)
        response = instruments_candles.response
        df = pd.DataFrame([candle["bid"] for candle in response["candles"]], dtype=np.float64)
        df['v'] = [candle["volume"] for candle in response["candles"]]
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df['date'] = [candle["time"] for candle in response["candles"]]
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        # print(df)
        for i in range(int(count/10)):
            mpf.plot(df[i*10:(i+1)*10], type='candle', style='nightclouds', savefig=f'data/candles{i}.png')
        # mpf.show()

    except V20Error as e:
        print("Error: {}".format(e))

if __name__ == '__main__':
    main()