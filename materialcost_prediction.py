import pandas as pd
import numpy as np
import streamlit as st
import datetime
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

uni_cost_1 = 0
uni_cost_2 = 0
uni_cost_3 = 0
uni_cost_4 = 0
uni_cost_5 = 0

# alogrithm
def LongShortTM(df, type, split):
    # creating dataframe
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0, len(df)), columns=["Date", type])

    for i in range(0, len(data)):
        new_data["Date"][i] = data["Date"][i]
        new_data[type][i] = data[type][i]

    # setting index
    new_data.index = new_data.Date
    new_data.drop("Date", axis=1, inplace=True)

    # creating train and test sets
    dataset = new_data.values

    train = dataset[0:split, :]
    valid = dataset[split:, :]

    # converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60, len(train)):
        x_train.append(scaled_data[i - 60 : i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss="mean_squared_error", optimizer="adam")
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    # predicting 246 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - 60 :].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(60, inputs.shape[0]):
        X_test.append(inputs[i - 60 : i, 0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    price = model.predict(X_test)
    price = scaler.inverse_transform(price)

    # rmse = np.sqrt(np.mean(np.power((valid - price), 2)))
    # st.write('RMSE value on validation set:')
    # st.write(rmse)

    # for plotting
    train = new_data[:split]
    valid = new_data[split:]
    valid["Predictions"] = price

    # append_data = DataFrame(data={type: [], 'Predictions': []})

    # append_data[type] = train[type]
    # append_data['Predictions'] = train[type]
    pic = valid[["Predictions"]]

    st.line_chart(pic)
    return valid[["Predictions"]]


# streamlit setting
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
st.write("With the available data")
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
genre = st.selectbox("Choose Algorithm", ("LSTM", " "))
if genre == "LSTM":
    with st.spinner("Calculating predictions..."):
        C = LongShortTM(df, type, split)
    print(C)
    print(C.index)
    d = st.date_input(
        "The date you want to make the order:",
        pd.to_datetime(C.index[0]).date(),
        pd.to_datetime(C.index[0]).date(),
        pd.to_datetime(C.index[-1]).date(),
    )
    print(d)
    st.write("The date you want to make the order:", d)
    d += datetime.timedelta(days=1)
    t = d.strftime("%Y-%m-%d")
    print(t)
    t = pd.to_datetime(t)
    print(t)
    C.index = pd.to_datetime(C.index)
    print(C)
    st.write("The prediction cost on that day:", C.loc[t, ["Predictions"]])


##### output side###
material_cost = C.loc[t]
uni_cost_1 = 5 * material_cost
uni_cost_2 = 44 + material_cost
uni_cost_3 = 200 * 1.6 * material_cost
uni_cost_4 = 77 + 3 * material_cost - 10
uni_cost_5 = material_cost * 7.33
