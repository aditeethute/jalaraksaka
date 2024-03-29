# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s4Hy1TZYmvD7ws0AUv320BxVmecojv3b
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

df = pd.read_csv('dummydum.csv')


df = pd.read_csv('dummydum.csv', parse_dates=['DATE '], index_col='DATE ')

result = adfuller(df['BERTH_DEPTH'])
print("ADF Statistic:", result[0])
print("p-value:", result[1])

df['value_diff'] = df['BERTH_DEPTH'].diff().dropna()

order = (3, 1, 4)

model = ARIMA(df['BERTH_DEPTH'], order=order)
results = model.fit()

y = df['BERTH_DEPTH']
X = df.drop(['BERTH_DEPTH'], axis=1)
train_size = int(len(df) * 0.8)  # 80% for training
train, test = y[:train_size], y[train_size:]
plot_acf(train)
plt.title('Autocorrelation Function (ACF)')
plt.show()

plot_pacf(train,lags=1)
plt.title('Partial Autocorrelation Function (PACF)')
plt.show()
p = 4
d = 1
q = 2
model = ARIMA(train, order=(p, d, q))
fit_model = model.fit()
predictions = fit_model.predict(start=len(train), end=len(train) + len(test) - 1, typ='levels')

# Evaluate the model
mse = mean_squared_error(test, predictions)
print(f'Mean Squared Error: {mse}')

# Plot the actual vs. predicted values
plt.plot(test, label='Actual')
plt.plot(predictions.values, label='Predicted')
plt.legend()
plt.show()

forecast_steps = 3
forecast = results.get_forecast(steps=forecast_steps)

forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int()

plt.plot(df['BERTH_DEPTH'], label='Historical Data')
plt.plot(forecast_mean, color='red', label='Forecast')
plt.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='red', alpha=0.2, label='Confidence Interval')

plt.xlabel('Date')
plt.ylabel('Value')
plt.title('ARIMA Forecast')
plt.legend()
plt.show()
all_mean =[]
print("Forecast for the next", forecast_steps, "days:")
print(forecast_mean)


from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

actual_values = test
predicted_values = predictions.values
mae = mean_absolute_error(actual_values, predicted_values)
mse = mean_squared_error(actual_values, predicted_values)
rmse = np.sqrt(mse)

print("mae",mae)
print("mse",mse)
print("rmse",rmse)
ape = np.abs((actual_values - predicted_values) / actual_values) * 100

# Calculating Mean Absolute Percentage Error (MAPE)
mape = np.mean(ape)

print("MAPE:", mape)

mae_percentage = mae * 100
rmse_percentage = rmse * 100

print("MAE (%):", mae_percentage)
print("RMSE (%):", rmse_percentage)
print("MAPE (%):", mape)
import os
import warnings
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt # If you are working with dataframes
import joblib  # or any other library to load your model
import torch
import plotly.express as px
from torchvision import models, transforms
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import seaborn as sns
predictict_result = forecast_mean
def main():
    
    st.title("JALARAKSAKA")
    html_temp = """
    <div style="background-color:tomato;padding:15px"›
    <h2 style="color:white;text-align:center;"›UNVEILING THE DEPTH</h2>
    </div>"""
    warnings.filterwarnings('ignore')
    df = pd.read_csv('dummydum.csv')

    col1, col2 = st.columns((2))
    with col1:
        #BERTH_DEPTH = st.text_input("Berth sector","Enter the Berth sector")
        if st.button("Select an berth sector"):
            selected_option = st.selectbox("Choose an option", ["Berth A", "Berth B", "Berth C"])
            if selected_option == "Berth A":
                latitude = 76.455
                longtude = 9.56
    with col2:    
        st.map()

    with col1:
        if st.button("GET ANALYSIS"):
            answer = generate_analysis()
            print(answer)
            st.success(f"The above graph show the different relation for monitoring purpose")
   

    if st.button("ACCESS HISTORICAL DATA"):
        # Code to run when the button is clicked
        answer = generate_data()
        print(answer)
        st.success(f"Above dataset shows the data collect over last 3 months")

    if st.button("PREDICT"):
        # Code to run when the button is clicked
        answer = generate_answer()
        print(answer)
        st.success(f"the above table shows the prediction of depth of water over that berth location for next 3 days")


def generate_answer():
    for value in forecast_mean:
        if value <10.5:
            st.write("ALERT!! DREAGING IS NEEDED")
        if value <=10.2:
            st.write("HIGH ALERT!! DREADGING IS MUST")
        else: 
            st.write("SAFE ZONE!! NO DREADGING REQUIRED AT PARTICULAR TIME")

    predicts= pd.DataFrame(list(forecast_mean.items()), columns=['Date', 'Predicted_Mean']) 
    forecast_data = {'Date': ['2023-02-08', '2023-02-09', '2023-02-10'],
                 'Predicted_Mean': [12.617290, 11.390256, 11.228435]}
    dfm = pd.DataFrame(forecast_data)

# Display the DataFrame as a table in Streamlit
    st.table(dfm)



def generate_data():
    df = pd.read_csv('dummydum.csv')
    st.write(df)

def generate_analysis():
    
    st.subheader("DATE WISE TEMPARETURE")
    data = {'DATE': ['02-01-2023','02-02-2023','02-03-2023','02-04-2023','02-05-2023','02-06-2023','02-07-2023',],
            'TEMPERATURE': [25, 23, 29, 29, 25, 27, 28]}

    df = pd.DataFrame(data)

    fig = px.bar(df,x = "DATE", y = "TEMPERATURE", template = "seaborn")
    st.plotly_chart(fig,use_container_width=True)
    
    
    st.subheader("DATE WISE SEDIMENT FORMATION")
    data = {'DATE': ['02-01-2023','02-02-2023','02-03-2023','02-04-2023','02-05-2023','02-06-2023','02-07-2023',],
            'SEDIMENT FORMATION': [25, 23, 29, 29, 25, 27, 28]}
    df = pd.DataFrame(data)
    fig2 = px.bar(df,x = "DATE", y = "SEDIMENT FORMATION" , template="seaborn")
    st.plotly_chart(fig2)
    
    st.subheader("TRANSPORT AT PORT")
    data = {'Category': ['AT PORT', 'LEAVING PORT', 'EXPECTED AT PORT'],
            'Value': [24, 6, 10]}
    df = pd.DataFrame(data)

    fig3 = px.pie(df, names='Category', values='Value', title='Pie Chart')
    st.plotly_chart(fig3)

if __name__=="__main__":
    main()
