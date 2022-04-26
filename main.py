import streamlit as st

st.set_page_config(page_title="Supply Chain", layout="wide")
from multipage import MultiPage
from pages import csv_upload, user_input


# Title of the main page
st.title("Supply Chain Manager")
app = MultiPage()
app.df = None
app.add_page("Demand data input", csv_upload.app)
app.add_page("Supply chain information input", user_input.app)

# The main app
app.run()
