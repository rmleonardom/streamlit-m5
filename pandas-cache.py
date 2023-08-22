import streamlit as st 
import pandas as pd 

st.title('Streamlit con cache')
DATA_URL = 'dataset.csv'

@st.cache
def load_data(nrows):
    # create dataframe 'data' with N rows
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # return dataframe
    return data

#print text
data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done !")

#print dataframe
st.dataframe(data)
data_load_count = st.text('Total = ' + str(data.shape[0]))

