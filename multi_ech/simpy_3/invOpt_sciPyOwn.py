from simulation.simLostSalesOwn import simulate_network

# from simulation.simBackorder import simulate_network
import numpy as np
import scipy.optimize
import time

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=RuntimeWarning)

import tsf_util as tsf
import pandas as pd
import numpy as np

###INPUTS###
csv_location = "../../DataCoSupplyChainDataset.csv"
prod_column = "Product Card Id"
fac_column = "Order Region"
date_column = "shipping date (DateOrders)"
q_column = "Order Item Quantity"
############

# Data input
df = pd.read_csv(csv_location, encoding="ISO-8859-1")
print("Loaded data")
prod_list = list(set(df[prod_column]))
prod = 365
fac_list = list(set(df[df[prod_column] == prod][fac_column]))
print("Obtained lists")
df["date"] = pd.to_datetime(df[date_column]).dt.date
date_column = "date"
print("Started sorting...")
df = df.sort_values(by=["date"], ascending=True)

numNodes = 3

distName = [""]
distParams = [()]
print("About to iterate")
for f in fac_list[0 : numNodes - 1]:
    pdf = df[(df[prod_column] == prod) & (df[fac_column] == f)].copy()
    pdf = pdf.groupby("date").agg(count=pd.NamedAgg(column=q_column, aggfunc="sum"))
    print(f"Getting best distribution for {f}")
    dist, p, params = tsf.get_best_distribution(pdf["count"])
    distName.append(dist)
    distParams.append(params)
    print(
        f"For {f} the best distribution is {dist} with a p value of {p:.4f} and params {params}"
    )

defaultLeadTime = np.random.random_integers(3, 5, size=numNodes - 1)
defaultLeadTime = np.append(0, defaultLeadTime)
nodeNetwork = np.zeros((numNodes, numNodes))
for i in range(numNodes - 1):
    nodeNetwork[0, i + 1] = 1
serviceTarget = np.append(0.0, np.ones(numNodes - 1) * 0.95)

allData = {
    "dd": distName,
    "dp": distParams,
    "n": numNodes,
    "net": nodeNetwork,
    "dlt": defaultLeadTime,
    "sl": serviceTarget,
}


def getObj(initial_guess, args):

    distName, distParams, numNodes, nodeNetwork, defaultLeadTime, serviceTarget = (
        args["dd"],
        args["dp"],
        args["n"],
        args["net"],
        args["dlt"],
        args["sl"],
    )

    # Split the initial guess to get base stock and ROP
    excess_inventory_guess = initial_guess[: (numNodes - 1)]
    ROP_guess = initial_guess[(numNodes - 1) :]
    base_stock_guess = np.add(excess_inventory_guess, ROP_guess)

    # Insert the supply node's base stock
    baseStock = np.insert(base_stock_guess, 0, 10000)

    # Insert a zero ROP for the first source node
    ROP = np.insert(ROP_guess, 0, 0)

    # Initialize inventory level
    initialInv = 0.9 * baseStock

    replications = 20
    totServiceLevel = np.zeros(numNodes)
    totAvgOnHand = 0.0
    for i in range(replications):
        nodes = simulate_network(
            i,
            numNodes,
            nodeNetwork,
            initialInv,
            ROP,
            baseStock,
            distName,
            distParams,
            defaultLeadTime,
        )

        totServiceLevel = np.array(
            [totServiceLevel[j] + nodes[j].serviceLevel for j in range(len(nodes))]
        )  # convert list to array

        totAvgOnHand += np.sum([nodes[j].avgOnHand for j in range(len(nodes))])

    servLevelPenalty = np.maximum(
        0, serviceTarget - totServiceLevel / replications
    )  # element-wise max
    objFunValue = totAvgOnHand / replications + 1.0e6 * np.sum(servLevelPenalty)
    return objFunValue


niter = 1


def callbackF(xk):
    global niter
    print("{0:4d}    {1:6.6f}".format(niter, getObj(xk, allData)))
    niter += 1


######## Main statements to call optimization ########
excess_inventory_initial_guess = [100 for i in range(numNodes - 1)]
ROP_initial_guess = [100 for i in range(numNodes - 1)]
guess = excess_inventory_initial_guess + ROP_initial_guess  # concatenate lists

NUM_CYCLES = 10
TIME_LIMIT = 1440  # minutes
start_time = time.time()
print("\nMax time limit: " + str(TIME_LIMIT) + " minutes")
print("Max algorithm cycles: " + str(NUM_CYCLES) + " (50 iterations per cycle)")
print(
    "The algorithm will run either for "
    + str(TIME_LIMIT)
    + " minutes or "
    + str(NUM_CYCLES)
    + " cycles"
)
ctr = 1
elapsed_time = (time.time() - start_time) / 60.0
while ctr <= NUM_CYCLES and elapsed_time <= TIME_LIMIT:
    print("\nCycle: " + str(ctr))
    print("{0:4s}    {1:9s}".format("Iter", "Obj"))
    optROP = scipy.optimize.minimize(
        fun=getObj,
        x0=guess,
        args=allData,
        method="Nelder-Mead",
        callback=callbackF,
        options={"disp": True, "maxiter": 50},
    )
    guess = optROP.x
    ctr += 1
    elapsed_time = (time.time() - start_time) / 60.0

print("\nFinal objective: " + "{0:10.3f}".format(getObj(optROP.x, allData)))
print("\nFinal solution: " + str(optROP.x))
print("\nTotal time: " + "{0:3.2f}".format(elapsed_time) + " minutes")
