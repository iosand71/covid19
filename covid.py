#!/usr/local/bin/python3
# coding: utf-8
""" Covid 

Covid19 data analysis for italy

"""
import locale
import sys, getopt
import pandas as pd
import numpy as np
from datetime import datetime,timedelta

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
pd.options.display.float_format = '{:,.3f}'.format

data = pd.read_csv(url)
data.data = pd.to_datetime(data.data)
data['nuovi_decessi'] = data.deceduti.diff()
data['mortalita'] = data.deceduti / data.totale_casi
data['guariti'] = data.dimessi_guariti / data.totale_casi
data['ricoverati'] = data.totale_ospedalizzati / data.totale_casi
data['intensivi'] = data.terapia_intensiva / data.totale_casi

data_pct = data[data.columns.difference(['data','stato','note','note_it','note_en','casi_da_sospetto_diagnostico','casi_da_screening'])].pct_change()
data_pct.insert(0,'data', data.data)

statistics = data.loc[:,['data','totale_casi','totale_positivi','nuovi_positivi','variazione_totale_positivi','deceduti',
                         'nuovi_decessi','terapia_intensiva','totale_ospedalizzati','dimessi_guariti',
                         'tamponi','casi_testati']]
statistics.insert(0,'% mortalita', data.mortalita)
statistics.insert(0,'% intensivi', data.intensivi)
statistics.insert(0,'% ricoverati', data.ricoverati)
statistics.insert(0,'% guariti', data.guariti)

recap = pd.DataFrame({
    'Valore assoluto': [data.totale_casi.iloc[-1],data.totale_positivi.iloc[-1], data.nuovi_positivi.iloc[-1],
                        data.variazione_totale_positivi.iloc[-1], data.deceduti.iloc[-1],
                        data.nuovi_decessi.iloc[-1], data.terapia_intensiva.iloc[-1],
                        data.totale_ospedalizzati.iloc[-1], data.dimessi_guariti.iloc[-1],
                        data.tamponi.iloc[-1],data.casi_testati.iloc[-1], data.mortalita.iloc[-1], data.intensivi.iloc[-1],
                        data.ricoverati.iloc[-1], data.guariti.iloc[-1]],
    'Variazione tot rispetto a ieri': [data.totale_casi.diff().iloc[-1],data.totale_positivi.diff().iloc[-1], data.nuovi_positivi.diff().iloc[-1],
                                     data.variazione_totale_positivi.diff().iloc[-1], data.deceduti.diff().iloc[-1],
                                     data.nuovi_decessi.diff().iloc[-1], data.terapia_intensiva.diff().iloc[-1],
                                     data.totale_ospedalizzati.diff().iloc[-1], data.dimessi_guariti.diff().iloc[-1],
                                     data.tamponi.diff().iloc[-1],data.casi_testati.diff().iloc[-1], data.mortalita.diff().iloc[-1],
                                     data.intensivi.diff().iloc[-1], data.ricoverati.diff().iloc[-1],
                                     data.guariti.diff().iloc[-1]],
    'Variazione % rispetto a ieri': [data_pct.totale_casi.iloc[-1],data_pct.totale_positivi.iloc[-1], data_pct.nuovi_positivi.iloc[-1],
                                     data_pct.variazione_totale_positivi.iloc[-1], data_pct.deceduti.iloc[-1],
                                     data_pct.nuovi_decessi.iloc[-1], data_pct.terapia_intensiva.iloc[-1],
                                     data_pct.totale_ospedalizzati.iloc[-1], data_pct.dimessi_guariti.iloc[-1],
                                     data_pct.tamponi.iloc[-1], data_pct.casi_testati.iloc[-1], data_pct.mortalita.iloc[-1],
                                     data_pct.intensivi.iloc[-1], data_pct.ricoverati.iloc[-1],
                                     data_pct.guariti.iloc[-1]]

}, index=['Totale casi','Attualmente positivi','Variazione totale casi', 'Variazione attualmente positivi', 'Totale decessi',
             'Variazione decessi','Terapia intensiva','Ospedalizzati','Dimessi','Totale tamponi','Casi testati',
             'Mortalità', 'Critici', 'Ricoverati','Guariti'])

pivot = pd.pivot_table(statistics, columns=['data'])
pivot.sort_values(axis = 1, by=['data'], ascending=False, inplace=True)
pivot.columns = pivot.columns.strftime('%d/%m/%Y')

updated_at = data.data.iloc[-1].strftime('%d/%m/%Y')

def dictionary():
  for name in data.columns:
    print(name)

def daily_stats():
    """ Daily stats for covid19 in Italy """

    def print_last_day(label, column):
      last = data[column].iloc[-1]
      pct_var = data_pct[column].iloc[-1]
      print(label, f'{last:20,.0f}', end='')
      print(f'{pct_var:+20.2%}')

    def print_as_pct(label, column):
      pct = data[column].iloc[-1]
      pct_pct = data_pct[column].iloc[-1]
      print(label, f'{pct:20.2%}', end='')
      print(f'{pct_pct:+20.2%}')

    # Data model:
    # ricoverati_con_sintomi terapia_intensiva totale_ospedalizzati 
    # isolamento_domiciliare totale_positivi variazione_totale_positivi 
    # nuovi_positivi dimessi_guariti deceduti totale_casi tamponi casi_testati 
    # note_it note_en casi_da_sospetto_diagnostico casi_da_screening

    print("Aggiornamento: ", updated_at, "\t\t\tvariazione rispetto a ieri")
    print("----------------------------------------------------------------------------")
    print_last_day("Totale casi: \t\t", 'totale_casi')
    print_last_day("Variaziohe casi: \t", 'nuovi_positivi')
    print_last_day("Totale positivi: \t", 'totale_positivi')
    print_last_day("Variazione positivi: \t", 'variazione_totale_positivi')
    print_last_day("Totale decessi: \t", 'deceduti')
    print_last_day("Variazione decessi: \t", 'nuovi_decessi')
    print_last_day("Terapia intensiva: \t", 'terapia_intensiva')
    print_last_day("Ospedalizzati: \t\t", 'totale_ospedalizzati')
    print_last_day("Dimessi: \t\t", 'dimessi_guariti')
    print_last_day("Totale tamponi: \t", 'tamponi')
    print_last_day("Totale testati: \t", 'casi_testati')
    print()

    print_as_pct("Morti: \t\t\t", 'mortalita')
    print_as_pct("Critici: \t\t", 'intensivi')
    print_as_pct("Ricoverati: \t\t", 'ricoverati')
    print_as_pct("Guariti: \t\t", 'guariti')
    print()

def base_seir_model(init_vals, params, t):
    """
    Params value for coronavirus (estimates)
      alpha = 0.57 # inverse of incubation period (0.210) 1/5.3 days
      beta = 1.2 # averate contact rate of the population (0.005)
      gamma = 0.449 # inverse of mean infection period (0.11) 1/2.9
      R0 = beta / gamma (2.6 - 4.34)

      initial values:
      S_0 = 1 - 222/60360000 # susceptibles
      E_0 = 1 / 60360000 # exposed
      I_0 = 200 # infected
      R_0 = 2.44 # recovered
    """
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (beta*S[-1]*I[-1])*dt
        next_E = E[-1] + (beta*S[-1]*I[-1] - alpha*E[-1])*dt
        next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
        next_R = R[-1] + (gamma*I[-1])*dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    return np.stack([S, E, I, R]).T

def seir_model_with_soc_dist(init_vals, params, t):
    """ rho = social distancing percentage """
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma, rho = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (rho*beta*S[-1]*I[-1])*dt
        next_E = E[-1] + (rho*beta*S[-1]*I[-1] - alpha*E[-1])*dt
        next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
        next_R = R[-1] + (gamma*I[-1])*dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    return np.stack([S, E, I, R]).T

def main(argv):
  help_str = 'usage: covid.py'
  locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')
  try:
    opts = getopt.getopt(argv, "h:")
  except getopt.GetoptError:
      print (help_str)
      sys.exit(2)
  for opt in opts:
    if opt == '-h':
      print (help_str)
      sys.exit()
  daily_stats()

if __name__ == "__main__":
   main(sys.argv[1:])

# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
