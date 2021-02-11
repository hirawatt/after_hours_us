import streamlit as st
import time
from datetime import datetime
import base64
import os
from dotenv import load_dotenv
import requests
from tabulate import tabulate

from data import after_hours_usa

st.set_page_config(page_title='After Hrs US Data', page_icon=None, layout='centered', initial_sidebar_state='auto')

load_dotenv()
token = os.getenv('DISCORD_WEBHOOK_AFTER_HOURS')

st.title('After Hours Volume as a Percentage of Float')
with st.empty():
    st.write(f"⏳ Data is being Processed")
    my_dataframe = after_hours_usa()
    st.write("✔️ Data Processed")

st.dataframe(my_dataframe)
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    #filename ="after_hrs{}.csv"
    href = f'<a href="data:file/csv;base64,{b64}" download="after_hrs.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(my_dataframe), unsafe_allow_html=True)

tabular_data = tabulate(my_dataframe, tablefmt="grid")
msg = {
    "content": tabular_data
    }
x = requests.post(token, data = msg)
st.write(x)

st.write('''
## Join [Discord Server](https://discord.gg/S37AEY4TKN) for updates and data notifications.
''')
