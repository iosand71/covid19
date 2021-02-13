# Dashboard Covid19 Italia

Esercizio di dearruginimento con python e pandas

- dati dierni con variazione percentuale rispetto al giorno precedente
- dati ultimi 7 giorni
- grafici andamento con tab per scala logaritmica e variazioni percentuali
- analisi predittiva variazione casi con fbprophet
- stima statistica di Rt e analisi predittiva
- pubblicazione automatica report statici su github

dipendenze gestite con poetry:

https://python-poetry.org/docs/#installation

- poetry install
- poetry run ...

## Riga di comando

```
Usage: covid [OPTIONS]

  Daily stats for covid19 in Italy.

  Available regions: Abruzzo, Basilicata, Calabria, Campania, Emilia-
  Romagna, 'Friuli Venezia Giulia', Lazio, Liguria, Lombardia, Marche,
  Molise, 'P.A. Bolzano', 'P.A. Trento', Piemonte, Puglia, Sardegna,
  Sicilia, Toscana, Umbria, "Valle d'Aosta", Veneto.

Options:
  -r, --region TEXT  Specify a region.
  --rt               Estimate Rt.
  --help             Show this message and exit.
```

### Credits

Per la stima di Rt  (metodo Bettencout & Ribeiro) il codice è preso da
questo articolo di Kevin Systrom: http://systrom.com/blog/the-metric-we-need-to-manage-covid-19/

Jupyter Notebook: https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb
