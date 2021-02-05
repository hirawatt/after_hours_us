import pandas as pd
from IPython.display import display
import requests
import yahoo_fin.stock_info as si
import streamlit as st

st.title('After Hours Volume as a Percentage of Float')

#@st.cache(suppress_st_warning=True)
def after_hours_usa():
    # Get After Hours Data from Source
    after_hours_url = 'https://www.marketwatch.com/tools/screener/after-hours'

    # Symbol     Company Name    After HoursPrice    After HoursVol      After HoursChg      After HoursChg %
    df = pd.read_html(after_hours_url)[2]
    st.dataframe(df)

    # List of Ticker Symbols
    tickers = df['Symbol'].tolist()

    #  Company Name      After HoursVol
    data_df = df[['Company Name', 'After HoursVol']]

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

    # Float Shares      Symbol
    df3 = df2.join(df0)

    # Company Name      After HoursVol      Float Shares        Stock Symbol
    final_df = data_df.join(df3)
    return final_df

my_dataframe = after_hours_usa()
st.dataframe(my_dataframe)
