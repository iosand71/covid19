#!/usr/bin/python3
# coding: utf-8
import locale
import sys, getopt
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import FunctionTransformer
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib

# Config

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
days_range = 50
order = 3
log_scale = False

# Implementation

tick = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
data = pd.read_csv(url)
data.data = pd.to_datetime(data.data)
data['nuovi_decessi'] = data.deceduti.diff()
data['mortalita'] = data.deceduti / data.totale_casi
data['guariti'] = data.dimessi_guariti / data.totale_casi
data['ricoverati'] = data.totale_ospedalizzati / data.totale_casi
data['intensivi'] = data.terapia_intensiva / data.totale_casi
data_pct = data[data.columns.difference(['data','stato','note_it','note_en'])].pct_change()
updated_at = data.data.iloc[-1].strftime('%d/%m/%Y')
locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')

def main(argv):
  global log_scale
  global days_range
  help_str = 'usage: covid.py [-l | --logmode] [-d | --days]'
  try:
    opts, args = getopt.getopt(argv, "hld:", ["logmode", "days="])
  except getopt.GetoptError:
      print (help_str)
      sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print (help_str)
      sys.exit()
    if opt in ('-l', '--logmode'):
      log_scale = True
    if opt in ('-d', '--days'):
      days_range = int(arg)

if __name__ == "__main__":
   main(sys.argv[1:])

def fmt_plot(aplot, size):
  global log_scale

  aplot.grid(which='major', color='#999999', linestyle='--')
  aplot.grid(which='minor', color='#CCCCCC', linestyle=':')
  aplot.set(xlabel="Giorni dal 24/02/2020")
  aplot.yaxis.set_major_formatter(tick)
  aplot.xaxis.set_major_locator(MultipleLocator(5))
  aplot.xaxis.set_minor_locator(AutoMinorLocator(5))
  if log_scale:
    return aplot
  aplot.yaxis.set_major_locator(MultipleLocator(size))
  aplot.yaxis.set_minor_locator(AutoMinorLocator(5))
  return aplot

def thousands(value):
  return f'{value:,}'

def print_last_result(label, column):
  global data
  global data_pct
  last = data[column].iloc[-1]
  pct_var = data_pct[column].iloc[-1]
  tabs = '\t' if last >= 100000 else '\t\t'
  print(label, thousands(last), end='\t')
  print(f' {tabs}( {pct_var:+.2%} )')

def print_pct(label, column):
  pct = data[column].iloc[-1]
  pct_pct = data_pct[column].iloc[-1]
  tabs = '\t\t\t' if pct <= 0.1 else '\t\t'
  print(label, f'{pct:.2%}', end='')
  print(f' {tabs}( {pct_pct:+.2%} )')

def start():
  global data
  # Data model:
  #   'data', 'stato', 'ricoverati_con_sintomi', 'terapia_intensiva',
  #   'totale_ospedalizzati', 'isolamento_domiciliare', 'totale_positivi',
  #   'variazione_totale_positivi', 'nuovi_positivi', 'dimessi_guariti',
  #   'deceduti', 'totale_casi', 'tamponi', 'note_it', 'note_en'

  print("Aggiornamento: ", updated_at, "\t\tvariazione rispetto a ieri")
  print("------------------------------------------------------------------")
  print_last_result("Totale casi: \t\t", 'totale_casi')
  print_last_result("Totale nuovi casi: \t", 'nuovi_positivi')
  print_last_result("Variazione nuovi casi: \t", 'variazione_totale_positivi')
  print_last_result("Totale decessi: \t", 'deceduti')
  print_last_result("Variazione decessi: \t", 'nuovi_decessi')
  print_last_result("Terapia intensiva: \t", 'terapia_intensiva')
  print_last_result("Ospedalizzati: \t\t", 'totale_ospedalizzati')
  print_last_result("Dimessi: \t\t", 'dimessi_guariti')
  print_last_result("Totale tamponi: \t", 'tamponi')
  print()
  print_pct("Mortalità: \t\t", 'mortalita')
  print_pct("Critici: \t\t", 'intensivi')
  print_pct("Ricoverati: \t\t", 'ricoverati')
  print_pct("Guariti: \t\t", 'guariti')

  plt.rcParams['figure.figsize'] = [18, 6]

  plots = data \
    .loc[:,['totale_casi','variazione_totale_positivi', 'terapia_intensiva',
            'totale_ospedalizzati','deceduti','dimessi_guariti','nuovi_decessi',
            'nuovi_positivi','tamponi']] \
    .plot(kind='line',
            subplots=True,
            sharex=True,
            layout=(3,3),
            grid=True,
            legend=True,
            logy=log_scale)

  plt_casi = fmt_plot(plots[0][0], 20000)
  plt_positivi = fmt_plot(plots[0][1], 1000)
  plt_intensivi = fmt_plot(plots[0][2], 1000)
  plt_ricoverati = fmt_plot(plots[1][0], 10000)
  plt_deceduti = fmt_plot(plots[1][1], 2000)
  plt_dimessi = fmt_plot(plots[1][2], 5000)
  plt_nuovi_decessi = fmt_plot(plots[2][0], 200)
  plt_nuovi = fmt_plot(plots[2][1], 1000)
  plt_tamponi = fmt_plot(plots[2][2], 100000)
  plt.suptitle("Covid19 Dati DPC del " + updated_at)

  # Ask for graphs
  print()
  res = input("Vuoi vedere i grafici? (y/N) ").lower() 
  if (res != 'y'):
    exit(1)
  plt.show()

  # Plot percentage variations by day

  tick = matplotlib.ticker.FuncFormatter(lambda x, p: format(x, '.0%'))
  plot_pct = data_pct \
    .loc[:,['totale_casi','variazione_totale_positivi', 'terapia_intensiva',
            'totale_ospedalizzati','deceduti','dimessi_guariti','nuovi_decessi',
            'nuovi_positivi','tamponi']] \
    .plot(kind='bar',
            subplots=True,
            sharex=True,
            layout=(3,3),
            grid=True,
            legend=True)

  plt_casi = fmt_plot(plot_pct[0][0], .5).yaxis.set_major_formatter(tick)
  plt_positivi = fmt_plot(plot_pct[0][1], .5).yaxis.set_major_formatter(tick)
  plt_intensivi = fmt_plot(plot_pct[0][2], .5).yaxis.set_major_formatter(tick)
  plt_ricoverati = fmt_plot(plot_pct[1][0], .5).yaxis.set_major_formatter(tick)
  plt_deceduti = fmt_plot(plot_pct[1][1], .5).yaxis.set_major_formatter(tick)
  plt_dimessi = fmt_plot(plot_pct[1][2], .5)
  plt_dimessi.yaxis.set_major_formatter(tick)
  plt_dimessi.set_ylim([-0.5,2])
  plt_nuovi_decessi = fmt_plot(plot_pct[2][0], .5).yaxis.set_major_formatter(tick)
  plt_nuovi = fmt_plot(plot_pct[2][1], .5).yaxis.set_major_formatter(tick)
  plt_tamponi = fmt_plot(plot_pct[2][2], .5).yaxis.set_major_formatter(tick)

  plt.suptitle("Covid19 Variazioni percentuali al " + updated_at)
  plt.show()

  # Plot regression analysis on total cases

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
  plt.figure()
  plt.rcParams['figure.figsize'] = [10, 6]

  if log_scale:
    plt.semilogy()

  fmt_plot(plt.gca(), 20000)
  plt.ylabel("Numero casi")
  plt.ylim(1, 150000)

  # Regression analysis
  coefficients = np.polyfit(x.values, data.totale_casi.values, order)
  poly = np.poly1d(coefficients)
  coefficients2 = np.polyfit(x.values, data.totale_ospedalizzati.values, order)
  poly2 = np.poly1d(coefficients2)
  coefficients3 = np.polyfit(x.values, data.terapia_intensiva.values, order)
  poly3 = np.poly1d(coefficients3)

  plt_scatter = plt.scatter(x,data.totale_casi,label="Totale casi", color="blue")
  plt_scatter2 = plt.scatter(x,data.totale_ospedalizzati, label="Ospedalizzati", color="green")
  plt_scatter3 = plt.scatter(x,data.terapia_intensiva, label="Terapia intensiva", color="orange")
  # plt_exp = plt.plot(pred_x, np.exp(y_fit), label="Regressione esponenziale")
  plt_poly = plt.plot(pred_x, poly(pred_x))
  plt_poly2 = plt.plot(pred_x, poly2(pred_x))
  plt_poly3 = plt.plot(pred_x, poly3(pred_x))

  plt.legend()
  plt.ylim(0, poly(pred_x).max().item() * 1.1)
  plt.suptitle("Covid19 Dati DPC del " + updated_at)
  plt.title("Regressione polinomiale, grado=" + str(order))

  plt.show()

start()
