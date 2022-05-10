import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=RuntimeWarning)

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.optimize import curve_fit
import pandas as pd
import streamlit as st


@st.cache(suppress_st_warning=True)
def load_csv(route, encoding="ISO-8859-1"):
    df = pd.read_csv(route, encoding=encoding)
    return df


def get_cont_dist():
    return [a[0] for a in stats._distr_params.distcont]


def get_discrete_dist():
    return [a[0] for a in stats._distr_params.distdiscrete]


@st.cache(suppress_st_warning=True)
def get_params(dist_name, data):
    if dist_name in get_cont_dist():
        dist = getattr(stats, dist_name)
        param = dist.fit(data)
    elif dist_name in get_discrete_dist():
        dist = getattr(stats, dist_name)
        # print(data)
        bins = int(np.arange(max(data))) - 0.5
        entries, bin_edges, _ = plt.hist(data, bins=bins, density=True)
        plt.close()
        bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        succ = False
        try:
            param, _ = curve_fit(lambda k: dist.pmf(k), bin_middles, entries)
            succ = True
        except:
            pass

        if not succ:
            try:
                param, _ = curve_fit(lambda k, a: dist.pmf(k, a), bin_middles, entries)
                succ = True
            except:
                pass
        if not succ:
            try:
                param, _ = curve_fit(
                    lambda k, a, b: dist.pmf(k, a, b), bin_middles, entries
                )
                succ = True
            except:
                pass
        if not succ:
            try:
                param, _ = curve_fit(
                    lambda k, a, b, c: dist.pmf(k, a, b, c), bin_middles, entries
                )
                succ = True
            except:
                pass
        if not succ:
            try:
                param, _ = curve_fit(
                    lambda k, a, b, c, d: dist.pmf(k, a, b, c, d), bin_middles, entries
                )
                succ = True
            except:
                pass
        if succ:
            param = tuple(param)
    else:
        print(dist_name)
        raise ValueError("Distribution name not found")
    return param


@st.cache(suppress_st_warning=True)
def get_best_distribution(data):
    """
    Input: data as time series
    Output: best distribution in scipy, pvalue, best fit params
    """
    # tarda unos 2 mins
    cont_dist = get_cont_dist()
    cont_dist.remove("kstwo")
    cont_dist.remove("levy_stable")
    cont_dist.remove("studentized_range")
    discrete_dist = get_discrete_dist()
    dist_names = cont_dist + discrete_dist
    dist_results = []
    params = {}
    succ = True
    for dist_name in dist_names:
        # print(dist_name)
        param = get_params(dist_name, data)
        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        _, p = stats.kstest(data, dist_name, args=param)
        # print("p value for "+dist_name+" = "+str(p))
        dist_results.append((dist_name, p))

    # select the best fitted distribution
    best_dist, best_p = max(dist_results, key=lambda item: item[1])

    return best_dist, best_p, params[best_dist]


@st.cache(suppress_st_warning=True)
def get_best_distribution_fast(data, min_p=0.99):
    """
    Input: data as time series
    Output: best distribution in scipy, pvalue, best fit params
    """
    cont_dist = ["chi", "expon", "f", "cauchy", "norm", "t"]
    # discrete_dist = ["poisson", "binom"]
    dist_names = cont_dist  # + discrete_dist
    dist_results = []
    params = {}
    for dist_name in dist_names:
        # print(dist_name)
        param = get_params(dist_name, data)
        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        _, p = stats.kstest(data, dist_name, args=param)
        # print("p value for "+dist_name+" = "+str(p))
        dist_results.append((dist_name, p))
        if p > min_p:
            break

    # select the best fitted distribution
    best_dist, best_p = max(dist_results, key=lambda item: item[1])

    return best_dist, best_p, params[best_dist]


@st.cache(suppress_st_warning=True)
def EBO(s, dist_name, *args):
    # Credits go to Professor Gentsch in ORIE 4160/5160
    dist = getattr(stats, dist_name)

    if dist_name in get_discrete_dist():
        epsilon = 0.999999
        x = s + 1
        tempsum = 0
        while dist.cdf(x, *args) < epsilon:
            prob = dist.pmf(x, *args)
            tempsum = tempsum + (x - s) * prob
            x += 1
    elif dist_name in get_cont_dist():
        mu = dist.mean(*args)
        sigma = dist.std(*args)
        term1 = sigma * (dist.pdf(s, *args))
        term2 = (mu - s) * (1 - dist.cdf(s, *args))
        tempsum = term1 + term2
    else:
        raise ValueError("Distribution name not found")

    return tempsum


@st.cache(suppress_st_warning=True)
def inventory_cost(s, h, b, dist_name, *args):
    dist = getattr(st, dist_name)
    dist = dist(*args)
    mu = dist.mean()
    return h * (s - mu) + (h + b) * EBO(s, dist_name, *args)


@st.cache(suppress_st_warning=True)
def prepare_df_pareto(df, prod_c, count_c, loc_c):
    df = df.loc[:, [loc_c, prod_c, count_c]]
    df = df.groupby(prod_c).agg(
        count=pd.NamedAgg(column="Order Item Quantity", aggfunc="sum")
    )
    df = df.sort_values(by="count", ascending=False)
    return df


@st.cache(suppress_st_warning=True)
def pareto(df, show=False):
    df["cumperc"] = df["count"].cumsum() / df["count"].sum()
    pareto = {}
    for p in df.index:
        pareto[p] = (df["count"][p], df["cumperc"][p])

    if show:
        fig, ax = plt.subplots()
        ax.bar(list(range(len(df.index))), df["count"])
        ax2 = ax.twinx()
        ax2.plot(list(range(len(df.index))), df["cumperc"], color="red")
        plt.show()
    return pareto


# @st.cache(suppress_st_warning=True)
def aggregate(df, aggcol, sumcol):
    # loc_list = list(set(df[aggcol]))
    loc_list = df[aggcol].unique()
    a = np.zeros(len(loc_list))
    locs = pd.DataFrame(data=a, index=loc_list, columns=["Units Sold"])
    for l in loc_list:
        q = int(np.sum(df.loc[df[aggcol] == l, sumcol]))
        locs.loc[l, ["Units Sold"]] = q
    return locs
