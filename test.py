import streamlit as st
import pandas as pd
from pages import testp1
from multipage import MultiPage

app = MultiPage()

# Title of the main page
st.title("Data Storyteller Application")
st.write("Upload your data")
f = st.file_uploader(
    label="Upload the orders' csv", type=["csv"], accept_multiple_files=False
)
if f != None:
    df = pd.read_csv(f)
    st.write(df)

# Add all your applications (pages) here
app.add_page("Hola", testp1.app)


# The main app
app.run()
