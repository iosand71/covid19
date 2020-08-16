# Dashboard Covid19 Italia

Esercizio di dearruginimento con python e pandas

- statistiche odierne con variazione percentuale rispetto al giorno precedente
- statistiche ultimi 7 giorni
- grafici andamento con tab per scala logaritmica
- grafici delle variazioni percentuali nel tempo
- analisi predittiva variazione casi con fbprophet
- stima statistica di Rt e analisi predittiva
- pubblicazione report statico su github

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

## Stima parametri modello SIR (con covsirphy)

|      | Type   |   Start   |     End    | Population  | ODE  | rho      | sigma    | tau  |  Rt   | 1/beta [day] | 1/gamma [day]  | RMS log error |
|------|--------|-----------|------------|-------------|------|----------|----------|------|-------|--------------|----------------|---------------|
|1st   | Past   |25Mar2020  |02Apr2020   | 60483973    | SIR  | 0.002552 | 0.000891 | 48   | 2.87  |  13          |  37            | 0.0262631     |
|2nd   | Past   |03Apr2020  |15Apr2020   | 60483973    | SIR  | 0.001394 | 0.000761 | 48   | 1.83  |  23          |  43            | 0.0191152     |
|3rd   | Past   |16Apr2020  |24Apr2020   | 60483973    | SIR  | 0.000949 | 0.000930 | 48   | 1.02  |  35          |  35            | 0.00866645    |
|4th   | Past   |25Apr2020  |08May2020   | 60483973    | SIR  | 0.000516 | 0.000945 | 48   | 0.55  |  64          |  35            | 0.0368156     |
|5th   | Past   |09May2020  |20May2020   | 60483973    | SIR  | 0.000379 | 0.001276 | 48   | 0.30  |  88          |  26            | 0.0181047     |
|6th   | Past   |21May2020  |09Jun2020   | 60483973    | SIR  | 0.000289 | 0.001386 | 48   | 0.21  | 115          |  24            | 0.0245434     |
|7th   | Past   |10Jun2020  |26Jul2020   | 60483973    | SIR  | 0.000421 | 0.001268 | 48   | 0.33  |  79          |  26            | 0.225918      |
|8th   | Future |27Jul2020  |01Jan2021   | 60483973    | SIR  | 0.000421 | 0.001268 | 48   | 0.33  |  79          |  26            | -             |
