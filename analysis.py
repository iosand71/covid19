#!/usr/bin/python3
# coding: utf-8
import locale
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import FunctionTransformer
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
data = pd.read_csv(url)
days_range = 40

dates = pd.to_datetime(data.data)
updated_at = data.data.values[-1]
updated_fmt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S").strftime('%d/%m/%Y')

locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')
def thousands(value):
  return f'{value:n}'

print("Aggiornamento: ", updated_fmt)
print("---------------")
print("Nuovi casi: ", thousands(data.nuovi_attualmente_positivi.values[-1]))
print("Nuovi decessi: ", thousands(data.deceduti.values[-1] - data.deceduti.values[-2]))
print("Totale casi: ", thousands(data.totale_casi.values[-1]))
print("Totale decessi: ", thousands(data.deceduti.values[-1]))

plt.rcParams['figure.figsize'] = [16, 24]
sns.set(style='whitegrid')
tick = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))

plots = data \
  .loc[:,['data','totale_casi','nuovi_attualmente_positivi','totale_ospedalizzati','deceduti']] \
  .plot(kind='line', 
          subplots=True, 
          sharex=False,
          layout=(2,2),
          grid=True, 
          legend=True, 
          logy=False)

plt_casi = plots[0][0]
plt_positivi = plots[0][1]
plt_ricoverati = plots[1][0]
plt_deceduti = plots[1][1]

# Set layout for totale casi
plt_casi.xaxis.set_major_locator(MultipleLocator(5))
plt_casi.yaxis.set_major_locator(MultipleLocator(10000))
plt_casi.yaxis.set_major_formatter(tick)
plt_casi.xaxis.set_minor_locator(AutoMinorLocator(5))
plt_casi.yaxis.set_minor_locator(AutoMinorLocator(5))
plt_casi.grid(which='major', color='#999999', linestyle='--')
plt_casi.grid(which='minor', color='#CCCCCC', linestyle=':')

# Set layout for nuovi positivi
plt_positivi.xaxis.set_major_locator(MultipleLocator(5))
plt_positivi.yaxis.set_major_locator(MultipleLocator(1000))
plt_positivi.yaxis.set_major_formatter(tick)
plt_positivi.xaxis.set_minor_locator(AutoMinorLocator(5))
plt_positivi.yaxis.set_minor_locator(AutoMinorLocator(5))
plt_positivi.grid(which='major', color='#999999', linestyle='--')
plt_positivi.grid(which='minor', color='#CCCCCC', linestyle=':')

# Set layout for totale ospedalizzati
plt_ricoverati.xaxis.set_major_locator(MultipleLocator(5))
plt_ricoverati.yaxis.set_major_locator(MultipleLocator(10000))
plt_ricoverati.yaxis.set_major_formatter(tick)
plt_ricoverati.xaxis.set_minor_locator(AutoMinorLocator(5))
plt_ricoverati.yaxis.set_minor_locator(AutoMinorLocator(5))
plt_ricoverati.grid(which='major', color='#999999', linestyle='--')
plt_ricoverati.grid(which='minor', color='#CCCCCC', linestyle=':')

# Set layout for deceduti
plt_deceduti.xaxis.set_major_locator(MultipleLocator(5))
plt_deceduti.yaxis.set_major_locator(MultipleLocator(1000))
plt_deceduti.yaxis.set_major_formatter(tick)
plt_deceduti.xaxis.set_minor_locator(AutoMinorLocator(5))
plt_deceduti.yaxis.set_minor_locator(AutoMinorLocator(5))
plt_deceduti.grid(which='major', color='#999999', linestyle='--')
plt_deceduti.grid(which='minor', color='#CCCCCC', linestyle=':')

# In[7]:
print()
print("Data graphs ...")
input("Press Enter to continue")
plt.suptitle("Covid19 DPC Data for " + updated_fmt)
plt.show()

x = data.index
y = data.totale_casi

def exponential_model(x,a,b,c):
    return a * np.exp(-b * x) + c
transformer = FunctionTransformer(np.log, validate=True)

# Exponential fit regression
x_reshaped = x.values.reshape(-1,1)
y_reshaped = y.values.reshape(-1,1)
y_trans = transformer.fit_transform(y_reshaped)
pred_x = np.linspace(0, days_range, days_range)
pred_x_reshape = pred_x.reshape(-1,1)
model = LinearRegression().fit(x_reshaped, y_trans)     
y_fit = model.predict(pred_x_reshape)

# Plot setup
plt.figure(2)
plt.rcParams['figure.figsize'] = [16, 10]
sns.set(style='whitegrid')
plt.rc('font', size=14)
ax = plt.gca()
tick = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
ax.yaxis.set_major_formatter(tick)
# Change major ticks to show every 20.
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(10000))
# Change minor ticks to show every 5. (20/4 = 5)
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.grid(which='major', color='#999999', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')
plt.grid(drawstyle='steps',in_layout=True)
plt.xlabel("Days since beginning")
plt.ylabel("Total number of infected people")
plt.ylim(1,150000)
# plt.semilogy()
# Real data
plt1 = plt.scatter(x,y,label="Real data",color="red")
# Predicted exponential curve

order = 4
coefficients = np.polyfit(x.values, y.values, order)
poly = np.poly1d(coefficients)

plt2 = plt.plot(pred_x, np.exp(y_fit), label="Exponential model")
plt3 = plt.plot(pred_x, poly(pred_x), label="Polynomial model, order=" + str(order))
plt.legend()
plt.suptitle("Covid19 DPC Data for " + datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S").strftime('%d/%m/%Y'))
plt.title("Regression analysis")

plt.show()

