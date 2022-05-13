import math
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats
import tsf_util as tu
from streamlit_multipage import MultiPage


def p_user_input(st, **state):

    st.title("Supply Chain analysis")
    if "product" not in state.keys() or "location" not in state.keys():
        st.error(
            "Product-Location pair not selected. Please return to 'Demand Data Input' page and within the 'Demand analysis for given product-location pair' choose a product and location and save at the end"
        )
    else:

        prod = state["product"]
        loc = state["location"]
        mean = state["mean"]
        std = state["standard deviation"]
        dist_name = state["distribution name"]
        dist_params = state["distribution parameters"]
        msg = (
            "Performing analysis for chosen product-location pair "
            + str(prod)
            + "-"
            + str(loc)
        )
        st.write(msg)

        st.header("Product Detail Information")

        Total_demand = mean * 365
        if "holding cost" not in state.keys():
            holding_cost = st.number_input("Please input the holding cost($/unit)")
            MultiPage.save({"holding cost": holding_cost})
        else:
            holding_cost = state["holding cost"]
            holding_cost = st.number_input(
                "Please input the holding cost($/unit)", value=holding_cost
            )
            MultiPage.save({"holding cost": holding_cost})

        st.write("Current holding cost is $", holding_cost, "/unit")
        st.write("\n")

        if "bo cost" not in state.keys():
            bo_cost = st.number_input("Please input the back order cost($/unit)")
            MultiPage.save({"bo cost": bo_cost})
        else:
            bo_cost = state["bo cost"]
            bo_cost = st.number_input("Please input the bo cost($/unit)", value=bo_cost)
            MultiPage.save({"bo cost": bo_cost})

        st.write("current backorder cost is $", bo_cost, "/unit")
        st.write("\n")

        logistic_option = st.selectbox(
            "What is its delivery method?", ("Marine Shipping", "Air Cargo")
        )
        st.write("You selected:", logistic_option)

        if logistic_option == "Marine Shipping":
            shipping_time = 30
            shipping_cost = 0.05
        if logistic_option == "Air Cargo":
            shipping_time = 2
            shipping_cost = 20
        st.write("Current shipping cost is $", shipping_cost, "/unit")
        st.write("Current shipping time is ", shipping_time, "days")

        st.write("\n")
        st.write("\n")
        if holding_cost != 0 and bo_cost != 0:
            critical_ratio = bo_cost / (bo_cost + holding_cost)
            st.write("Most ecnomical fill rate", round(critical_ratio, 2) * 100, "%")
        if "service level" not in state.keys():
            service_level = st.slider(
                "What is the fill Rate you want to achieve", 0, 100, 25
            )
            MultiPage.save({"service level": service_level})
        else:
            service_level = state["service level"]
            service_level = st.slider(
                "What is the fill Rate you want to achieve", 0, 100, service_level
            )
            MultiPage.save({"service level": service_level})
        st.write("Current Fill rate is", service_level, "%")

        # target_inv = shipping_time * mean + stats.norm.ppf(service_level / 100) * std
        # order_size = shipping_time * mean
        # average_inv = (target_inv + (stats.norm.ppf(service_level / 100) * std)) / 2
        # order_times = int(365 / shipping_time)
        # inv_cost = average_inv * shipping_time * order_times * holding_cost
        # operation_cost = inv_cost + order_times * shipping_cost
        # st.write("\n")
        # st.write("\n")

        # col1, col2, col3 = st.columns(3)
        # col1.metric(label="Target inventory  of product 1", value=int(target_inv))
        # col2.metric(label="Inventory cost of product 1", value=int(inv_cost))
        # col3.metric(label="Operation cost of product 1", value=int(operation_cost))
        # x = np.linspace(0, 100, 100)
        # y_list = []
        # for i in range(1, 100):
        #     t_inv = shipping_time * mean + stats.norm.ppf(i / 100) * std
        #     a_inv = (t_inv + (stats.norm.ppf(i / 100) * std)) / 2
        #     o_times = int(365 / shipping_time)
        #     i_cost = a_inv * shipping_time * o_times * holding_cost
        #     y = i_cost + o_times * shipping_cost
        #     y_list.append(y)
        # st.line_chart(y_list)

        with st.expander("Outputs and Recommendations"):
            if holding_cost != 0 and bo_cost != 0:
                # c1, c2 = st.columns(2)
                ############## c1 ###############
                target_inv = (
                    shipping_time * mean + stats.norm.ppf(service_level / 100) * std
                )
                order_size = shipping_time * mean
                average_inv = (
                    target_inv + (stats.norm.ppf(service_level / 100) * std)
                ) / 2
                order_times = int(365 / shipping_time)
                inv_cost = average_inv * shipping_time * order_times * holding_cost
                operation_cost = inv_cost + order_times * shipping_cost
                st.subheader("Target Inventory Policy")
                st.subheader("Ordering")
                msg = "Most economical order size is " + str(int(order_size)) + " units"
                st.write(msg)
                # msg = (
                #     "Which would mean ordering "
                #     + str(order_times)
                #     + " times per year or ordering every "
                #     + str(365 / order_times)
                #     + " days"
                # )
                # st.write(msg)
                st.write(
                    "Which would mean ordering ",
                    order_times,
                    " times per year or ordering every ",
                    365 / order_times,
                    " days",
                )
                st.subheader("Customer Service")
                # msg = (
                #     "Average fill rate will be "
                #     + str(service_level)
                #     + " meaning around "
                #     + str((1 - service_level) * Total_demand)
                #     + " orders won't be successfully satisfied"
                # )
                # st.write(msg)
                st.write(
                    "Average fill rate will be ",
                    service_level,
                    " meaning around ",
                    (1 - service_level / 100) * Total_demand,
                    " orders won't be successfully satisfied",
                )

                st.subheader("Inventory Management")
                # msg = "The target inventory level will be " + str(target_inv)
                # st.write(msg)
                st.write("The target inventory level will be ", target_inv)

                st.subheader("Financial Implications")
                # msg = (
                #     "With this strategy the inventory costs will be $ "
                #     + str(inv_cost)
                #     + " and total operation costs will be $ "
                #     + str(operation_cost)
                # )
                # st.write(msg)
                st.write(
                    "With this strategy the inventory costs will be ",
                    inv_cost,
                    " and total operation costs will be ",
                    operation_cost,
                )
                st.write(
                    "Below we show the operation cost curve for different service levels"
                )
                x = np.linspace(0, 100, 100)
                y_list = []
                for i in range(1, 100):
                    t_inv = shipping_time * mean + stats.norm.ppf(i / 100) * std
                    a_inv = (t_inv + (stats.norm.ppf(i / 100) * std)) / 2
                    o_times = int(365 / shipping_time)
                    i_cost = a_inv * shipping_time * o_times * holding_cost
                    y = i_cost + o_times * shipping_cost
                    y_list.append(y)
                st.line_chart(y_list)
                # ########################## c2 ######################
                # EOQ = np.sqrt(2 * shipping_cost * Total_demand / holding_cost)
                # dist = getattr(stats, dist_name)
                # dist = dist(*dist_params)
                # ss = dist.ppf(service_level / 100) * std * math.sqrt(shipping_time)
                # EBO = tu.EBO(target_inv, dist_name, *dist_params)
                # average_inv = (ss + EOQ) / 2
                # order_times = Total_demand / EOQ
                # inv_cost = average_inv * shipping_time * order_times * holding_cost
                # operation_cost = inv_cost + order_times * shipping_cost

                # c2.subheader("Target Inventory Policy")
                # c2.subheader("Ordering")
                # msg = "Most economical order size is " + str(int(order_size)) + " units"
                # c2.write(msg)
                # msg = (
                #     "Which would mean ordering "
                #     + str(order_times)
                #     + " times per year or ordering every "
                #     + str(365 / order_times)
                #     + " days"
                # )
                # c2.write(msg)
                # c2.subheader("Customer Service")
                # msg = (
                #     "Average fill rate will be "
                #     + str(service_level)
                #     + " meaning around "
                #     + str((1 - service_level) * Total_demand)
                #     + " orders won't be successfully satisfied"
                # )
                # c2.write(msg)

                # c2.subheader("Inventory Management")
                # msg = (
                #     "The reorder point level will be "
                #     + str(ss)
                #     + " units, with an order quantity of "
                #     + str(EOQ)
                #     + " which lead to an average inventory of "
                #     + str(average_inv)
                # )
                # c2.write(msg)

                # c2.subheader("Financial Implications")
                # msg = (
                #     "With this strategy the inventory costs will be "
                #     + str(inv_cost)
                #     + " and total operation costs will be "
                #     + str(operation_cost)
                # )
                # c2.write(msg)

                # c2.write(
                #     "For the given fill rate of",
                #     service_level,
                #     "% a total of",
                #     EBO,
                #     "backorders a year are expected",
                # )
        ##### Out Put Section #####
        # inv_all = inv_cost + inv_cost_2 + inv_cost_3 + inv_cost_4 + inv_cost_5
        # operation_all = (
        #     operation_cost
        #     + operation_cost_2
        #     + operation_cost_3
        #     + operation_cost_4
        #     + operation_cost_5
        # )
