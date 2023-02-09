import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math
import yfinance as yf

### Read the the csv document from the previous E file ###
adoptions_cumulative_raw = pd.read_csv("/Users/octavianciupitu/Desktop/EPP Final/adoptions_cumulative_raw.csv")
# Date column needs to be attached:
adoptions_cumulative_raw['Date'] = pd.date_range(start = '22/07/2019', end = '26/12/2022', freq = 'W-MON')

# We define the time frame that we want to analyze
# We decide to cut off the first 55 entries auf the data, because during this time the Helium Network
# was still young, and therefore the adoption process had not yet started rolling at that point.
# The analyzed timeframe is: 2020-08-10 to 2020-12-26.
min_range = 55
max_range = 180
adoptions_cumulative = adoptions_cumulative_raw[min_range:max_range]

# We devide the data into a train and test dataset.
adoptions_train = adoptions_cumulative[0:65]
adoptions_test = adoptions_cumulative[64:125]

# We compute the first difference of the cumulative sales to explore the amount of new adoptions per week.
new_adoptions = adoptions_train.HotspotsWeek.diff().iloc[1:]

plt.rcParams['font.size'] = 14

plt.figure().set_figwidth(10)
plt.plot(adoptions_train.Date.iloc[1:], new_adoptions)
#plt.title("Weekly Hotspot Adoptions")
#plt.xlabel("Date")
plt.ylabel("Number of Adoptions")
plt.savefig('plots/weekly_hotspot_adoptions')
plt.clf()

# We also plot the chart with the amount of cumulative adoptions every week,
plt.figure().set_figwidth(10)
plt.plot(adoptions_train.Date, adoptions_train.HotspotsWeek)
#plt.title("Weekly Hotspot Adoptions (Cumulative)")
#plt.xlabel("Date")
plt.ylabel("Number of Adoptions")
plt.savefig('plots/weekly_hotspot_adoptions_cumulative')
plt.clf()

# Preparing the variables that are needed to run the Linear Regression, which is subsequently needed
# to calculate the coeffictien of innovation (p), coefficient of imitation (q) and the market size (m)
adoptions_ts = adoptions_train.HotspotsWeek[0:len(adoptions_train)-1]

Y = adoptions_ts-adoptions_ts[min_range]# Series that contains the amount of the total amount of past
                                        # adoptions. We substract the first entry of the series from
                                        # all entries to achieve a better model fit
Ysq = Y**2 # The quadratic term of the Bass model

X = np.transpose(np.array([Y, Ysq])) # Combining both variables into an ndarray for the linear regression

# Run the regression:
reg = LinearRegression().fit(X,new_adoptions)

# Extract the coefficients in order to calculate the Bass Model parameters p, q and m_
a = reg.intercept_
b = reg.coef_[0]
c = reg.coef_[1]

# Calculate the Bass Model Parameters using the formulas from the literature:
m = (-b - math.sqrt(b**2-4*a*c))/(2*c)
p = a/m
q = b + p

def bass_model(p,q,m,T):
    """Creates estimated adoption data based on actual adoption data.

    Args:
        p (float): Coefficient of innovation, calculated from the linear regression results.
        q (float): Coefficient of immitation, calculated from the linear regression results.
        m (float): Parameter that indicated the market size and provides the scale of the demand forecast. Also calculated from the linear regression results.
        T (float): The timeframe for which the estimated time series should be returned

    Returns:
        ndarray: Contains adoptions per week estimated by the bass model. 
    """
    A = np.zeros(T)
    Y = np.zeros(T+1)

    for t in range(T):
        A[t] = p*m + (q-p) * Y[t] - (q/m) * Y[t]**2
        Y[t+1] = Y[t] + A[t]
    
    return A

# First, we are fitting the bass model with the same length as the train dataset. This way, we compare
# the actual data with our bass model fit
adoptions = bass_model(p,q,m,len(adoptions_train))

plt.figure().set_figwidth(10)
plt.plot(adoptions_train.Date, adoptions, label = "Fitted Bass Model")
plt.plot(adoptions_train.Date.iloc[1:], new_adoptions, label = "Actual New Hotspot Adotions")
#plt.title("Bass Model Adoptions vs Actual Adoptions")
#plt.xlabel("Date")
plt.ylabel("Number of Adoptions")
plt.legend(loc="lower left", bbox_to_anchor=(0.01,0.77))
plt.savefig('plots/bass_model_adoptions_vs_actual_adoptions')
plt.clf()

# Now, we are predicting the bass model for the whole timeframe. 
adoptions_pred = bass_model(p,q,m,len(adoptions_cumulative))

# Transforming the ndarray to cumulative data (since the bass model only returns number of new
# adoptions per week) and adding back the previously discarded adoptions.
adoptions_pred_cumul = np.cumsum(adoptions_pred) + adoptions_ts[min_range]

# Plot the whole bass model fit, which is only based on the adoptions_train dataset:
plt.figure().set_figwidth(10)
plt.plot(adoptions_cumulative.Date, adoptions_pred_cumul, label = "Fitted Bass Model") 

# Also plot the adoption_train dataset:
plt.plot(adoptions_train.Date, adoptions_train.HotspotsWeek, label = "Actual Cumulative Hotspot Adotions")

#plt.title("Cumulative Bass Model Adoptions vs Actual Cumulative Adoptions")
#plt.xlabel("Date")
plt.ylabel("Number of Adoptions")
plt.xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
plt.legend(loc="lower left", bbox_to_anchor=(0.01,0.77))
plt.savefig('plots/cumulative_bass_model_adoptions_vs_actual_cumulative_adoptions')

plt.clf()

# Finally, plot the the adoptions_test dataset, which the model has never seen before and compare
# it to the prediction
plt.figure().set_figwidth(10)
plt.plot(adoptions_cumulative.Date, adoptions_pred_cumul, label = "Fitted Bass Model") 
plt.plot(adoptions_train.Date, adoptions_train.HotspotsWeek, label = "Actual Cumulative Hotspot Adotions (Train)")
plt.plot(adoptions_test.Date, adoptions_test.HotspotsWeek, label = "Actual Cumulative Hotspot Adotions (Test)")

#plt.title("Predicted Cumulative Weekly Hotspot Adoptions")
#plt.xlabel("Date")
plt.ylabel("Number of Adoptions")
plt.xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
plt.legend(loc="lower left", bbox_to_anchor=(0.01,0.7))
plt.savefig('plots/predicted_cumulative_weekly_hotspot_adoptions')

plt.clf()

# Create the final plot that is comparing the Diffusion Graph (Adoption Graph) to the historical
# price data of HNT (data from yahoo finance)

HNT_ticker = yf.Ticker("HNT-USD")
HNT_data = HNT_ticker.history(period="3y", interval = '1wk')

HNT_data['Date'] = HNT_data.index

HNT_data_filtered = HNT_data[(HNT_data['Date'] > '2020-08-09') & (HNT_data['Date'] < '2022-12-27')]

x = HNT_data_filtered.Date
y1 = adoptions_pred_cumul
y2 = adoptions_cumulative.HotspotsWeek
y3 = HNT_data_filtered.Close

fig, ax1 = plt.subplots()

ax1.plot(x, y1, 'darkblue', label = "Predicted Adoptions")

ax2 = ax1.twiny()
ax2.plot(x, y2, 'royalblue', label = "Actual Adoptions")

ax3 = ax1.twinx()
ax3.plot(x, y3, 'green', label = "HNT Price")

ax1.set_ylabel("Adoptions", color = "blue")
ax3.set_ylabel("Price", color = "green")

ax1.tick_params(axis='y', colors = "blue")
ax3.tick_params(axis='y', colors = "green")

ax3.spines['right'].set_color('green')
ax3.spines['left'].set_color('blue')

ax1.set_xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])
ax2.set_xticks(["2020-10", "2021-04", "2021-10", "2022-04", "2022-10"])

fig.set_figwidth(10)
fig.legend(loc="lower left", bbox_to_anchor=(0.13,0.65))

plt.savefig('plots/hnt_comparison')
plt.clf()
