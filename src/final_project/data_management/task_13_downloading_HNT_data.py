"""Downloading historical price data of HNT (data from yahoo finance)."""

import pytask
import pandas as pd
#if there is no yfinance installed on your computer then first run 
# $ pip install yfinance
import yfinance as yf

from final_project.config import BLD


@pytask.mark.produces(
    {
        "HNT_data": BLD / "data" / "HNT_data.csv",
    }
    )

def task_13_downloading_HNT_data(produces):
    HNT_ticker = yf.Ticker("HNT-USD")
    HNT_data = HNT_ticker.history(period="3y", interval = '1wk')
    HNT_data['Date'] = HNT_data.index
    HNT_data_filtered = HNT_data[(HNT_data['Date'] > '2020-08-09') & (HNT_data['Date'] < '2022-12-27')]
    HNT_data_filtered.to_csv(produces['HNT_data'])