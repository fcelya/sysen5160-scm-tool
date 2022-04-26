import streamlit as st
from streamlit_multipage import MultiPage
import pandas as pd
import numpy as np
from scipy import stats

st.set_page_config(page_title="Supply Chain", layout="wide")


def p_welcome(st, **state):
    a, b = 3, 3
    c1, c2 = st.columns([a, b])
    c2.image("./media/welcome.jpg")
    c1.title("Supply Chain Wizard")
    c1.subheader("")
    c1.subheader("")
    c1.subheader("")
    c1.subheader(f"Stop overpaying and underperforming.")
    c1.subheader("Step up your Supply Chain game")


def p_load_csv(st, **state):
    st.title("Load the demand data")

    f = st.file_uploader("Load here your demand data as a .csv", type=[".csv"])
    if f != None:
        df = pd.read_csv(f, encoding="ISO-8859-1")
        st.write(df.head())

    st.subheader(
        "Write the header of the following columns as written in your .csv file"
    )

    c1, c2, c3 = st.columns(3)
    _, sc2, _ = st.columns(3)

    product_c = c1.text_input(label="Product Identifier Column")
    count_c = c2.text_input(label="Amount Bought Per Order Column")
    location_c = c3.text_input(label="Location Identifier Column")

    if f != None and product_c != None and count_c != None and location_c != None:
        if sc2.button("Check and save data"):
            f1, f2, f3 = False, False, False
            if product_c in df.columns:
                c1.success("Product column found!")
                f1 = True
            else:
                c1.error("Please check the product column name spelling")
            if count_c in df.columns:
                c2.success("Sales count column found!")
                f2 = True
            else:
                c2.error("Please check the sales count column name spelling")
            if location_c in df.columns:
                c3.success("Location column found!")
                f3 = True
            else:
                c3.error("Please check the location column name spelling")
            if f1 and f2 and f3:
                MultiPage.save(
                    {
                        "df": df,
                        "product column": product_c,
                        "count column": count_c,
                        "location column": location_c,
                    }
                )


def p_user_input(st, **state):
    st.title("Input Interface")

    mean = 100
    std = 5

    holding_cost = st.number_input("Please input the holding cost($/unit)")
    st.write("current holding cost is $", holding_cost, "/unit")
    st.write("\n")

    bo_cost = st.number_input("Please input the back order cost($/unit)")
    st.write("current backorder cost cost is $", bo_cost, "/unit")
    st.write("\n")

    logistic_option = st.selectbox(
        "What is the delivery method", ("Marine Shipping", "Air Cargo")
    )
    st.write("You selected:", logistic_option)

    if logistic_option == "Marine Shipping":
        shipping_time = 10
        shipping_cost = 0.5
    if logistic_option == "Air Cargo":
        shipping_time = 2
        shipping_cost = 20
    st.write("Current shipping cost is $", shipping_cost, "/unit")
    st.write("Current shipping time is ", shipping_time, "days")
    if holding_cost != 0 and bo_cost != 0:
        EOQ = np.sqrt(2 * shipping_cost * mean / holding_cost)
        st.write("Most economical order size", int(EOQ), "units")
    else:
        EOQ = 0

    st.write("\n")
    st.write("\n")
    if holding_cost != 0 and bo_cost != 0:
        critical_ratio = bo_cost / (bo_cost + holding_cost)
        st.write("Most ecnomical fill rate", round(critical_ratio, 2) * 100, "%")
    else:
        critical_ratio = 0
    service_level = st.slider("What is the fill Rate you want to achieve", 0, 100, 25)
    st.write("Current Fill rate is", service_level, "%")

    target_inv = shipping_time * mean + stats.norm.ppf(service_level / 100) * std
    # total_holding_cost =
    st.write("\n")
    st.write("\n")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory", value=int(target_inv))
    col2.metric(label="Target inventory", value=int(target_inv))
    col3.metric("Humidity", "86%", "4%")

    MultiPage.save(
        {
            "holding cost": holding_cost,
            "backorder cost": bo_cost,
            "shipping time": shipping_time,
            "shipping cost": shipping_cost,
            "EOQ": EOQ,
            "critical ratio": critical_ratio,
            "service level": service_level,
            "TIL": target_inv,
        }
    )

    pass


app = MultiPage()
app.st = st
app.add_app("Welcome to SCW!", p_welcome)
app.add_app("Demand data input", p_load_csv)
app.add_app("User data input", p_user_input)

app.run()
