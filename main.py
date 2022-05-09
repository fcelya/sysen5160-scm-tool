import streamlit as st
from streamlit_multipage import MultiPage
import pandas as pd
import numpy as np
from scipy import stats
import tsf_util as tu
import matplotlib.pyplot as plt

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

    c1, c2, c3, c4 = st.columns(4)
    _, sc2, _ = st.columns(3)

    product_c = c1.text_input(label="Product Identifier Column Name")
    count_c = c2.text_input(label="Amount Bought Per Order Column Name")
    location_c = c3.text_input(label="Location Identifier Column Name")
    date_c = c4.text_input(label="Date Column Name")

    if (
        f != None
        and product_c != None
        and count_c != None
        and location_c != None
        and date_c != None
    ):
        if sc2.button("Check and save data"):
            f1, f2, f3, f4 = False, False, False, False
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
            if date_c in df.columns:
                c4.success("Date column found!")
                f4 = True
            else:
                c4.error("Please check the date column name spelling")
            if f1 and f2 and f3 and f4:
                MultiPage.save(
                    {
                        "df": df,
                        "product column": product_c,
                        "count column": count_c,
                        "location column": location_c,
                        "date column": date_c,
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


def p_output(st, **state):
    df = state["df"]
    p_col = state["product column"]
    c_col = state["count column"]
    l_col = state["location column"]
    d_col = state["date column"]
    df = df.loc[:, [p_col, c_col, l_col, d_col]]
    df[d_col] = pd.to_datetime(df[d_col]).dt.date
    products = list(set(df[p_col]))
    locations = list(set(df[l_col]))

    with st.expander("Exploratory Analysis"):
        analysis = st.selectbox(
            "What kind of analysis would you like to do?",
            ["Per product", "Per location"],
        )
        if analysis == "Per product":
            prod = st.selectbox("What product do you want to analyse?", products)
            df2 = df.loc[df[p_col] == prod, :]
            locs = tu.aggregate(df2, l_col, c_col)
            locs = locs.sort_values(by="Units Sold", ascending=False)
            c1, c2 = st.columns(2)
            c1.write("This product has been sold at the following locations")
            c1.write(locs)

            locs["cumperc"] = locs["Units Sold"].cumsum() / locs["Units Sold"].sum()
            fig, ax = plt.subplots()
            ax.bar(list(range(len(locs.index))), locs["Units Sold"])
            ax2 = ax.twinx()
            ax2.plot(list(range(len(locs.index))), locs["cumperc"], color="red")
            ax2.set_ylim([0, 1])
            ax.set_xticks(range(len(locs)))
            ax.set_xticklabels(locs.index)
            ax.set_title("Pareto analysis of units sold")
            plt.setp(ax.get_xticklabels(), rotation=60, horizontalalignment="right")
            plt.tight_layout()
            c2.pyplot(fig)

        else:
            loc = st.selectbox("What location do you want to analyse?", locations)
            df2 = df.loc[df[l_col] == loc, :]
            prods = tu.aggregate(df2, p_col, c_col)
            prods = prods.sort_values(by="Units Sold", ascending=False)
            c1, c2 = st.columns(2)
            c1.write("This location has sold the following products")
            c1.write(prods)

            prods["cumperc"] = prods["Units Sold"].cumsum() / prods["Units Sold"].sum()
            fig, ax = plt.subplots()
            ax.bar(list(range(len(prods.index))), prods["Units Sold"])
            ax2 = ax.twinx()
            ax2.plot(list(range(len(prods.index))), prods["cumperc"], color="red")
            ax2.set_ylim([0, 1])
            ax.set_xticks(range(len(prods)))
            ax.set_xticklabels(prods.index)
            ax.set_title("Pareto analysis of units sold")
            plt.setp(ax.get_xticklabels(), rotation=60, horizontalalignment="right")
            plt.tight_layout()
            c2.pyplot(fig)

    with st.expander("Product-Location pair analysis"):
        prod = st.selectbox(
            "What product do you want to analyse?", products, key="prodpair"
        )
        loc = st.selectbox(
            "What location do you want to analyse?",
            list(set(df.loc[df[p_col] == prod, l_col])),
            key="locpair",
        )

        df3 = df.loc[df[p_col] == prod, :]
        df3 = df3.loc[df3[l_col] == loc, :]
        df3 = tu.aggregate(df3, d_col, c_col)
        df3.index = pd.to_datetime(df3.index)
        df3.asfreq("D", fill_value=0)
        # fig, ax = plt.subplots()
        fig, ax = df3.plot()
        st.pyplot(fig)
    pass


app = MultiPage()
app.st = st
app.add_app("Welcome to SCW!", p_welcome)
app.add_app("Demand data input", p_load_csv)
app.add_app("User data input", p_user_input)
app.add_app("Analysis output", p_output)

app.run()
