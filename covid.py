#!/usr/bin/python3
# coding: utf-8
import locale
import sys, getopt
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
# Config

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

# Implementation

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
  help_str = 'usage: covid.py'
  try:
    opts, args = getopt.getopt(argv, "hld:", ["logmode", "days="])
  except getopt.GetoptError:
      print (help_str)
      sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print (help_str)
      sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])

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
  print_last_result("Totale positivi: \t", 'totale_positivi')
  print_last_result("Totale decessi: \t", 'deceduti')
  print_last_result("Variazione decessi: \t", 'nuovi_decessi')
  print_last_result("Terapia intensiva: \t", 'terapia_intensiva')
  print_last_result("Ospedalizzati: \t\t", 'totale_ospedalizzati')
  print_last_result("Dimessi: \t\t", 'dimessi_guariti')
  print_last_result("Totale tamponi: \t", 'tamponi')
  print_last_result("Totale testati: \t", 'casi_testati')
  print()
  print_pct("Mortalità: \t\t", 'mortalita')
  print_pct("Critici: \t\t", 'intensivi')
  print_pct("Ricoverati: \t\t", 'ricoverati')
  print_pct("Guariti: \t\t", 'guariti')

  print()

start()
