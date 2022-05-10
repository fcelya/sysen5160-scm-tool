import streamlit as st
from streamlit_multipage import MultiPage


st.set_page_config(page_title="Supply Chain", layout="wide")

from pages.p_welcome import p_welcome
from pages.p_load_csv import p_load_csv
from pages.p_visual_analysis import p_visual_analysis
from pages.p_cost_prediction import p_cost_prediction
from pages.p_user_input import p_user_input

# # @st.cache(suppress_st_warning=True)
# def p_user_input(st, **state):
#     st.title("Input Interface")

#     mean = 100
#     std = 5

#     holding_cost = st.number_input("Please input the holding cost($/unit)")
#     st.write("current holding cost is $", holding_cost, "/unit")
#     st.write("\n")

#     bo_cost = st.number_input("Please input the back order cost($/unit)")
#     st.write("current backorder cost cost is $", bo_cost, "/unit")
#     st.write("\n")

#     logistic_option = st.selectbox(
#         "What is the delivery method", ("Marine Shipping", "Air Cargo")
#     )
#     st.write("You selected:", logistic_option)

#     if logistic_option == "Marine Shipping":
#         shipping_time = 10
#         shipping_cost = 0.5
#     if logistic_option == "Air Cargo":
#         shipping_time = 2
#         shipping_cost = 20
#     st.write("Current shipping cost is $", shipping_cost, "/unit")
#     st.write("Current shipping time is ", shipping_time, "days")
#     if holding_cost != 0 and bo_cost != 0:
#         EOQ = np.sqrt(2 * shipping_cost * mean / holding_cost)
#         st.write("Most economical order size", int(EOQ), "units")
#     else:
#         EOQ = 0

#     st.write("\n")
#     st.write("\n")
#     if holding_cost != 0 and bo_cost != 0:
#         critical_ratio = bo_cost / (bo_cost + holding_cost)
#         st.write("Most ecnomical fill rate", round(critical_ratio, 2) * 100, "%")
#     else:
#         critical_ratio = 0
#     service_level = st.slider("What is the fill Rate you want to achieve", 0, 100, 25)
#     st.write("Current Fill rate is", service_level, "%")

#     target_inv = shipping_time * mean + stats.norm.ppf(service_level / 100) * std
#     # total_holding_cost =
#     st.write("\n")
#     st.write("\n")

#     col1, col2, col3 = st.columns(3)
#     col1.metric(label="Target inventory", value=int(target_inv))
#     col2.metric(label="Target inventory", value=int(target_inv))
#     col3.metric("Humidity", "86%", "4%")

#     MultiPage.save(
#         {
#             "holding cost": holding_cost,
#             "backorder cost": bo_cost,
#             "shipping time": shipping_time,
#             "shipping cost": shipping_cost,
#             "EOQ": EOQ,
#             "critical ratio": critical_ratio,
#             "service level": service_level,
#             "TIL": target_inv,
#         }
#     )

#     pass


app = MultiPage()
app.st = st
app.navbar_style = "SelectBox"
app.add_app("Welcome to SCW!", p_welcome)
app.add_app("Demand Data Input", p_load_csv)
app.add_app("Visual Analysis", p_visual_analysis)
app.add_app("Cost Predictor", p_cost_prediction)
app.add_app("Supply Chain Analysis", p_user_input)
# app.add_app("Data visualization", p_dataviz)
# app.add_app("User data input", p_user_input)
# app.add_app("Analysis output", p_output)

app.run()
