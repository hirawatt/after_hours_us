import pandas as pd
from IPython.display import display
import requests
import yahoo_fin.stock_info as si
import streamlit as st
import math
from numpy import isnan

@st.cache(suppress_st_warning=True)
def after_hours_usa():
    # Get After Hours Data from Source
    after_hours_url = 'https://www.marketwatch.com/tools/screener/after-hours'

    # K M B T string values to numbers
    m = {'K': 3,'M': 6, 'B': 9,'T': 12}

    # Symbol     Company Name    After HoursPrice    After HoursVol      After HoursChg      After HoursChg %
    main_df = pd.read_html(after_hours_url)[2]

    # List of Ticker Symbols
    tickers = main_df['Symbol'].tolist()

    #  Company Name      After HoursVol
    data_df = main_df[['Company Name', 'After HoursVol']]

    # Get M B to numbers for After Hours Volume
    after_hoursvol = data_df['After HoursVol'].tolist()
    after_hoursvol_list = [int(float(i[:-1]) * 10 ** m[i[-1]]) for i in after_hoursvol]

    # Stock Symbol
    df0 = pd.DataFrame(tickers, columns=['Stock Symbol'])

    # Initializing DataFrame
    df2 = pd.DataFrame()

    # Get Data For all the Tickers
    for i in tickers:
        df = si.get_stats(i)
        df1 = df.loc[df['Attribute'] == 'Float']
        df2 = df2.append(df1, ignore_index=True)

    # Rename and Drop Columns of DataFrame
    df2 = df2.rename(columns={"Value":"Float Shares"}, errors="raise")
    df2 = df2.drop(columns=['Attribute'])

    # Get M B to numbers for float shares
    floatshares = df2['Float Shares'].tolist()
    float_list = [i if pd.isnull(i) else int(float(i[:-1]) * 10 ** m[i[-1]]) for i in floatshares]

    # After Hours Volume as a Percentage of Float Shares Calculation
    percentage = [after_hoursvol_list[i] / float_list[i] * 100 for i in range(len(float_list))]
    per_df = pd.DataFrame(percentage, columns=['Percentage'])

    # Float Shares      Symbol
    df3 = [df2, per_df, df0]

    # Company Name      After HoursVol      Float Shares        Stock Symbol
    final_df = data_df.join(df3)
    return final_df, main_df
