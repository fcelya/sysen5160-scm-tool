import pandas as pd
import tsf_util as tu
import matplotlib.pyplot as plt
import plotly.express as px
from scipy import stats
from streamlit_multipage import MultiPage
import numpy as np
import math

# @st.cache(suppress_st_warning=True)
def p_output(st, **state):
    df = state["df"]
    p_col = state["product column"]
    c_col = state["count column"]
    l_col = state["location column"]
    d_col = state["date column"]
    df = df.loc[:, [p_col, c_col, l_col, d_col]]
    df[d_col] = pd.to_datetime(df[d_col]).dt.date
    # products = list(set(df[p_col]))
    products = list(df[p_col].unique())
    # locations = list(set(df[l_col]))
    locations = list(df[l_col].unique())

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
            if st.button(
                "Do you want to continue the Supply Chain analysis for this product and location?"
            ):
                MultiPage.save(
                    {
                        "distribution name": dist_name,
                        "distribution parameters": params,
                        "mean": mean,
                        "standard deviation": sigma,
                    }
                )
                st.success("Distribution saved")

    pass
