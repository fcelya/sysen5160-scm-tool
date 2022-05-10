import pandas as pd
import numpy as np
import streamlit as st
import datetime
from scipy import stats
import tsf_util as tu


def p_cost_prediction(st, **state):
    uni_cost_1 = 0
    uni_cost_2 = 0
    uni_cost_3 = 0
    uni_cost_4 = 0
    uni_cost_5 = 0

    # streamlit setting
    st.title("Unit cost predictor")
    df = pd.read_csv(f"./test1.csv")  # you need to change the file-path for this code

    options = np.array(df["Date"]).tolist()

    (start_time, end_time) = st.select_slider(
        "Desired Time Length：",
        # min_value = datetime(2013, 10, 8,),
        # max_value = datetime(2018, 10, 8,),
        options=options,
        value=(
            "2013/10/8",
            "2018/10/8",
        ),
    )

    (start_time, end_time) == (
        "2013/10/8",
        "2018/10/8",
    )
    st.write("From:", end_time)
    st.write("To:", start_time)
    end_time = pd.to_datetime(end_time)
    start_time = pd.to_datetime(start_time)
    # setting index as date
    df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d")
    df.index = df["Date"]

    df = df[start_time:end_time]

    split = int(0.9 * len(df))

    st.subheader("Goal")
    type = st.selectbox("Choose your prediction goal：", ("UnitCost", "CarrierCost"))

    st.subheader("Algorithm")
    genre = st.selectbox("Choose Algorithm", ("LSTM",))
    if genre == "LSTM":
        with st.spinner("Calculating predictions..."):
            C = tu.LongShortTM(df, type, split)
        d = st.date_input(
            "The date you want to make the order:",
            pd.to_datetime(C.index[0]).date(),
            pd.to_datetime(C.index[0]).date(),
            pd.to_datetime(C.index[-1]).date(),
        )
        st.write("The date you want to make the order:", d)
        d += datetime.timedelta(days=1)
        t = d.strftime("%Y-%m-%d")
        t = pd.to_datetime(t)
        C.index = pd.to_datetime(C.index)
        st.write("The prediction cost on that day:", C.loc[t, ["Predictions"]])

    ##### output side###
    material_cost = C.loc[t]
    uni_cost_1 = 5 * material_cost
    uni_cost_2 = 44 + material_cost
    uni_cost_3 = 200 * 1.6 * material_cost
    uni_cost_4 = 77 + 3 * material_cost - 10
    uni_cost_5 = material_cost * 7.33
