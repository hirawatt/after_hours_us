import streamlit as st
from data import after_hours_usa

my_dataframe = after_hours_usa()
st.dataframe(my_dataframe)
st.write('''
## Join [Discord Server](https://discord.gg/S37AEY4TKN) for updates and data notifications.
''')
