# streamlit run /Users/chenkeshan/Documents/GitHub/sysen5160/5160_dashboard.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import tsf_util as tu
from streamlit_multipage import MultiPage
import math
from scipy import stats

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# @st.cache(suppress_st_warning=True)
def p_visual_analysis(st, **state):
    st.title("Visual Analysis")
    df = state["df"]
    p_col = state["product column"]
    c_col = state["count column"]
    l_col = state["location column"]
    d_col = state["date column"]

    with st.expander("Global analysis"):
        sns.set(style="ticks", color_codes=True)
        init_notebook_mode(connected=True)

        ## Graphs

        # delivery status
        ## pie
        data_delivery_status = (
            df.groupby(["Delivery Status"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot1 = px.pie(
            data_delivery_status,
            values="Number of Orders",
            names="Delivery Status",
            title="Delivery Status",
            width=500,
            height=500,
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )

        # Delivery Status -- Number of Orders [Order Region]
        ## bar

        data_delivery_status_region = (
            df.groupby(["Delivery Status", "Order Region"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot2 = px.bar(
            data_delivery_status_region,
            x="Delivery Status",
            y="Number of Orders",
            color="Order Region",
            title="Delivery Status in different Regions",
        )

        # Order Region - Number of Orders
        ## bar
        data_Region = (
            df.groupby(["Order Region"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=True)
        )
        plot3 = px.bar(
            data_Region,
            x="Number of Orders",
            y="Order Region",
            color="Number of Orders",
            title="Number of Orders in different Regions",
        )

        # Order country - Number of Orders
        ## bar
        data_countries = (
            df.groupby(["Order Country"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=True)
        )
        plot4 = px.bar(
            data_countries.head(20),
            x="Number of Orders",
            y="Order Country",
            color="Number of Orders",
            title="Number of Orders in different Countries",
        )

        # Order Country -- Sales of Orders
        ## bar
        df_sales_country = (
            df.groupby(["Order Country"])["Sales"]
            .sum()
            .reset_index(name="Sales of Orders")
            .sort_values(by="Sales of Orders", ascending=False)
        )
        plot5 = px.bar(
            df_sales_country.head(10),
            x="Order Country",
            y="Sales of Orders",
            color="Sales of Orders",
            title="Sales of Orders in different Countries",
        )

        # Order Country -- Profit of Orders
        ## Map
        df_geo = (
            df.groupby(["Order Country", "Order City"])["Order Profit Per Order"]
            .sum()
            .reset_index(name="Profit of Orders")
            .sort_values(by="Profit of Orders", ascending=False)
        )
        fig = px.choropleth(
            df_geo,
            locationmode="country names",
            locations="Order Country",
            color="Profit of Orders",  # lifeExp is a column of data
            hover_name="Order Country",
            # hover_data ='Order City',
            color_continuous_scale=px.colors.sequential.Plasma,
            width=1300,
            height=500,
        )

        # Customer Segments
        ## Pie
        data_Customer_Segment = (
            df.groupby(["Customer Segment"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot6 = px.pie(
            data_Customer_Segment,
            values="Number of Orders",
            names="Customer Segment",
            title="Number of Orders of different Customer Segments",
            width=500,
            height=500,
            color_discrete_sequence=px.colors.sequential.RdBu,
        )

        # Shipping Mode
        ## Pie
        data_shipping = (
            df.groupby(["Shipping Mode"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot7 = px.pie(
            data_shipping,
            values="Number of Orders",
            names="Shipping Mode",
            title="Number of Orders of different Shipping Mode",
            width=500,
            height=500,
            color_discrete_sequence=px.colors.sequential.Jet,
        )

        # Order Item Quantity - Number of Orders
        ## Pie
        data_order = (
            df.groupby(["Order Item Quantity"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot8 = px.bar(
            data_order,
            x="Order Item Quantity",
            y="Number of Orders",
            color="Number of Orders",
        )

        # Market
        ## Pie
        data_market = (
            df.groupby(["Market"])["Order Id"]
            .count()
            .reset_index(name="Number of Orders")
            .sort_values(by="Number of Orders", ascending=False)
        )
        plot9 = px.pie(
            data_market,
            values="Number of Orders",
            names="Market",
            title="Number of Orders of different Market",
            width=500,
            height=500,
            color_discrete_sequence=px.colors.sequential.Viridis,
        )

        # Order Sales in Region
        ## bar
        df_sales_region = (
            df.groupby(["Order Region"])["Sales"]
            .sum()
            .reset_index(name="Sales of Orders")
            .sort_values(by="Sales of Orders", ascending=False)
        )
        plot10 = px.bar(
            df_sales_region.head(10),
            x="Order Region",
            y="Sales of Orders",
            color="Sales of Orders",
            title="Sales of Orders in different Regions",
        )

        # Dashboard Layout

        #     st.set_page_config(
        #         page_title="Supply Chain Dashboard", layout="wide", page_icon="😄"
        #     )

        # st.markdown(
        #     "<h1 style='text-align: center; color: NavajoWhite;'>Supply Chain Data Visualization Dashboard</h1>",
        #     unsafe_allow_html=True,
        # )

        row11, row12, row13 = st.columns(3)
        st.markdown("<hr/>", unsafe_allow_html=True)  # add a horizontal line

        with row11:
            st.subheader("**Customer Segments**")
            st.plotly_chart(plot6, use_container_width=True)

        with row12:
            st.subheader("**Market**")
            st.plotly_chart(plot9, use_container_width=True)

        with row13:
            st.subheader("**Order Item Quantity**")
            st.plotly_chart(plot8, use_container_width=True)

        # with kpi3:
        #     st.markdown("**Third KPI**")
        #     number1 = 111
        #     st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}<h1>", unsafe_allow_html=True)

        st.subheader("**Order Sales in Areas**")
        row21, row22, row23, row24 = st.columns(4)
        with row21:
            st.plotly_chart(plot3, use_container_width=True)

        with row22:
            st.plotly_chart(plot10, use_container_width=True)

        with row23:
            st.plotly_chart(plot4, use_container_width=True)

        with row24:
            st.plotly_chart(plot5, use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)  # add a horizontal line

        st.subheader("**Profit of Order distributed in different Countries**")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr/>", unsafe_allow_html=True)  # add a horizontal line\

        st.subheader("**Order Shipping**")
        row31, row32, row33 = st.columns(3)
        with row31:
            st.plotly_chart(plot1, use_container_width=True)

        with row32:
            st.plotly_chart(plot2, use_container_width=True)

        with row33:
            st.plotly_chart(plot7, use_container_width=True)

    df = df.loc[:, [p_col, c_col, l_col, d_col]]
    df[d_col] = pd.to_datetime(df[d_col]).dt.date
    # products = list(set(df[p_col]))
    products = list(df[p_col].unique())
    # locations = list(set(df[l_col]))
    locations = list(df[l_col].unique())

    with st.expander("Pareto analysis per product or location"):
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

    with st.expander("Demand analysis for given product-location pair"):
        prod = st.selectbox(
            "What product do you want to analyse?", products, key="prodpair"
        )
        loc = st.selectbox(
            "What location do you want to analyse?",
            df.loc[df[p_col] == prod, l_col].unique(),
            key="locpair",
        )

        df3 = df.loc[df[p_col] == prod, :]
        df3 = df3.loc[df3[l_col] == loc, :]
        df3 = tu.aggregate(df3, d_col, c_col)
        df3.index = pd.to_datetime(df3.index)
        df3 = df3.asfreq("D", fill_value=0)
        df3 = df3.sort_index()

        (start_time, end_time) = st.select_slider(
            "What period would you like to analyze",
            # min_value = datetime(2013, 10, 8,),
            # max_value = datetime(2018, 10, 8,),
            options=df3.index.sort_values(ascending=True),
            value=(
                df3.index[-1],
                df3.index[0],
            ),
        )

        df4 = df3[start_time:end_time]
        plot = px.line(df4)
        st.plotly_chart(plot, use_container_width=True)

        with st.spinner("Calculating distribution..."):
            dist_name, pval, params = tu.get_best_distribution_fast(df4)
            st.write(
                "The most probable distribution is",
                dist_name,
                "with parameters",
                params,
                "with a probability of",
                pval,
            )
            dist = getattr(stats, dist_name)
            mean = dist.mean(*params)
            sigma = dist.std(*params)
            st.write(
                "This distribution has a mean of",
                mean,
                "and a standard deviation of",
                sigma,
            )
            print(mean, sigma)
            # st.warning()
            if (
                math.isnan(mean)
                or math.isnan(sigma)
                or math.isinf(mean)
                or math.isinf(sigma)
            ):
                mean = np.average(df4.values)
                sigma = np.std(df4.values)
                msg = (
                    "Since the mean and standard deviation could not be calculated for the given distribution, a normal distribution with mean "
                    + str(mean)
                    + " and standard deviation "
                    + str(sigma)
                    + " was assumed"
                )
                st.warning(msg)
                dist_name = "norm"
                params = (mean, sigma)
            if st.button("Save Product-Location pair and the given distribution"):
                MultiPage.save(
                    {
                        "product": prod,
                        "location": loc,
                        "distribution name": dist_name,
                        "distribution parameters": params,
                        "mean": mean,
                        "standard deviation": sigma,
                    }
                )
                st.success("Distribution saved")
