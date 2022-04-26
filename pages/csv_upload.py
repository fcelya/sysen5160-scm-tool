import streamlit as st
import pandas as pd

def app():
    st.write("Upload your data")
    f = st.file_uploader(
        label="Upload the orders' csv", type=["csv"], accept_multiple_files=False
    )
    if f != None:
        df = pd.read_csv(f)
        st.write(df.head())
        return df