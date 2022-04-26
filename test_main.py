import streamlit as st
from streamlit_multipage import MultiPage
import pandas as pd

st.set_page_config(page_title="Supply Chain", layout="wide")


def p_load_csv(st, **state):
    st.title("Load the demand data")

    f = st.file_uploader("Load here your demand data as a .csv", type=[".csv"])
    if f != None:
        df = pd.read_csv(f)
        MultiPage.save({"df": df})


app = MultiPage()
app.st = st
app.add_app("Demand data input", p_load_csv)

app.run()
