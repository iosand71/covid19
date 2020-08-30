#!/bin/bash

wget -q https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv -O ./data/covid19-italia.csv
wget -q https://github.com/pcm-dpc/COVID-19/raw/master/dati-regioni/dpc-covid19-ita-regioni.csv -O ./data/covid19-regioni.csv
wget -q https://github.com/pcm-dpc/COVID-19/raw/master/dati-province/dpc-covid19-ita-province.csv -O ./data/covid19-province.csv
