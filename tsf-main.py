# https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/
# https://towardsdatascience.com/an-overview-of-time-series-forecasting-models-a2fa7a358fcb
# https://towardsdatascience.com/7-libraries-that-help-in-time-series-problems-d59473e48ddd

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.tbats import TBATS
from sktime.utils.plotting import plot_series

###INPUTS###
csv_location = "./DataCoSupplyChainDataset.csv"
prod_id = 365
fperiods = 14
pwindows = [7, 30.42, 365]
############

# Data input
df = pd.read_csv(csv_location, encoding="ISO-8859-1")
# Basic metrics
prod_list = list(set(df["Product Card Id"]))
nprods = len(prod_list)
# Initial manipulations
df["Date"] = pd.to_datetime(df["shipping date (DateOrders)"]).dt.date
df_sorted = df.sort_values(by=["Date"], ascending=True).copy()
# Aggregate count extraction
prod_demand = {}
prod_demand[prod_id] = (
    df_sorted[df_sorted["Product Card Id"] == prod_id]
    .groupby("Date")
    .agg(count=pd.NamedAgg(column="Product Image", aggfunc="count"))
)
prod_demand[prod_id]["date"] = prod_demand[prod_id].index
prod_demand[prod_id].index = range(prod_demand[prod_id].index.size)

# Initial visualization
plt.plot(prod_demand[prod_id])
plt.rcParams["figure.figsize"] = (200, 50)
plt.rcParams["lines.linewidth"] = 10
plt.show()
# Data cleaning
for i in range(prod_demand[prod_id].index.size - 1):
    gap = (
        prod_demand[prod_id].loc[i + 1, "date"] - prod_demand[prod_id].loc[i, "date"]
    ).days
    if gap != 1:
        # print('in if',i,gap)
        for j in range(1, gap):
            data = {
                "count": [0],
                "date": prod_demand[prod_id].loc[i, "date"]
                + datetime.timedelta(days=j),
            }
            print("concating: ", data)
            prod_demand[prod_id] = prod_demand[prod_id].append(
                pd.DataFrame(data=data), ignore_index=True
            )
prod_demand[prod_id] = prod_demand[prod_id].sort_values(by=["date"])
prod_demand[prod_id].index = range(prod_demand[prod_id].index.size)

# Forecasting
cutoff = prod_demand[prod_id].iloc[-1, 1]
fh = ForecastingHorizon(
    pd.PeriodIndex(pd.date_range(str(cutoff), periods=fperiods, freq="D")),
    is_relative=False,
)

y = prod_demand[prod_id].copy()
y.index = pd.PeriodIndex(y["date"], freq="D")
y = y["count"]

forecaster = TBATS(sp=pwindows)
print("About to fit...")
forecaster.fit(y)
print("Fitted!")
y_pred = forecaster.predict(fh=fh)

# Display results
plot_series(y[-fperiods * 4 :], y_pred, labels=["y", "y_pred"])
print(y_pred)
