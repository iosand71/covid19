#!/usr/local/bin/python3
# coding: utf-8
""" Covid 

Covid19 data analysis for italy.

"""
import click
import locale
import numpy as np
import pandas as pd
from scipy import stats as sps
from scipy.interpolate import interp1d

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
url_regions = "https://github.com/pcm-dpc/COVID-19/raw/master/dati-regioni/dpc-covid19-ita-regioni.csv"
url_provinces = "https://github.com/pcm-dpc/COVID-19/raw/master/dati-province/dpc-covid19-ita-province.csv"
global_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
pd.options.display.float_format = '{:,.3f}'.format

# https://www.sciencedirect.com/science/article/pii/S1201971220301193
GAMMA = 1 / 4.6
R_T_MAX = 12
r_t_range = np.linspace(0, R_T_MAX, R_T_MAX * 100 + 1)
COLS = ['date', 'ricoverati_con_sintomi', 'totale_casi', 'totale_positivi', 'nuovi_positivi',
        'variazione_totale_positivi', 'deceduti',
        'nuovi_decessi', 'terapia_intensiva', 'totale_ospedalizzati', 'dimessi_guariti', 'isolamento_domiciliare',
        'casi_da_sospetto_diagnostico', 'casi_da_screening',
        'tamponi', 'casi_testati']

pd.set_option('mode.chained_assignment', None)


def add_columns(df):
    """ Add columns for new deaths and percentages.  """
    df.loc[:, 'date'] = df.index
    df.loc[:, 'nuovi_decessi'] = df.deceduti.diff()
    df.loc[:, 'mortalita'] = df.deceduti / df.totale_casi
    df.loc[:, 'guariti'] = df.dimessi_guariti / df.totale_casi
    df.loc[:, 'ricoverati'] = df.totale_ospedalizzati / df.totale_casi
    df.loc[:, 'intensivi'] = df.terapia_intensiva / df.totale_casi
    df.loc[:, 'tamponi_per_die'] = df.tamponi.diff()


def calc_statistics(df):
    """ Build cleaned up dataframe with just stats columns.  """
    stats = df.loc[:,
            ['date', 'totale_casi', 'totale_positivi', 'nuovi_positivi', 'variazione_totale_positivi', 'deceduti',
             'nuovi_decessi', 'terapia_intensiva', 'ingressi_terapia_intensiva','totale_ospedalizzati', 'dimessi_guariti',
             'tamponi', 'casi_testati']]
    stats.insert(0, '% mortalita', df.mortalita)
    stats.insert(0, '% intensivi', df.intensivi)
    stats.insert(0, '% ricoverati', df.ricoverati)
    stats.insert(0, '% guariti', df.guariti)

    return stats


def calc_percentages(df):
    """ Build dataframe with percent changes day to day.  """
    df_pct = df[df.columns.difference(['date', 'stato', 'note', 'note_it', 'note_en',
                                       'note_test', 'note_casi',
                                       'casi_da_sospetto_diagnostico', 'casi_da_screening',
                                       'totale_positivi_test_molecolare', 'totale_positivi_test_antigenico_rapido', 'tamponi_test_molecolare','tamponi_test_antigenico_rapido',
                                       'codice_nuts_1','codice_nuts_2',
                                       'codice_regione', 'denominazione_regione', 'lat', 'long'])].pct_change()
    df_pct.insert(0, 'data', df.date)

    return df_pct


def load_regional():
    """ Load regional dataset.  """
    global data_reg, data_reg_pct
    data_reg = pd.read_csv(url_regions, parse_dates=['data'], index_col=['data'])
    add_columns(data_reg)
    data_reg_pct = calc_percentages(data_reg)


def get_region(df, region):
    """ Extract a single region from regional dataset.  """
    return df[df.denominazione_regione == region]


def set_region(region):
    """ replace global data with specific region. """
    global data, data_reg
    data = get_region(data_reg, region)


def load_provincial():
    """ Load provincial dataset.  """
    global data_prov
    data_prov = pd.read_csv(url_provinces, parse_dates=['data'], index_col=['data'])


def load():
    """ Load national dataset. """
    global data
    data = pd.read_csv(url, parse_dates=['data'], index_col=['data'])

def calc_recap():
  recap = pd.DataFrame({
      'Valore assoluto': [data.totale_casi.iloc[-1], data.totale_positivi.iloc[-1], data.nuovi_positivi.iloc[-1],
                          data.variazione_totale_positivi.iloc[-1], data.deceduti.iloc[-1],
                          data.nuovi_decessi.iloc[-1], data.terapia_intensiva.iloc[-1],
                          data.totale_ospedalizzati.iloc[-1], data.dimessi_guariti.iloc[-1],
                          data.tamponi.iloc[-1], data.casi_testati.iloc[-1], data.mortalita.iloc[-1],
                          data.intensivi.iloc[-1],
                          data.ricoverati.iloc[-1], data.guariti.iloc[-1]],
      'Variazione tot rispetto a ieri': [data.totale_casi.diff().iloc[-1], data.totale_positivi.diff().iloc[-1],
                                         data.nuovi_positivi.diff().iloc[-1],
                                         data.variazione_totale_positivi.diff().iloc[-1], data.deceduti.diff().iloc[-1],
                                         data.nuovi_decessi.diff().iloc[-1], data.terapia_intensiva.diff().iloc[-1],
                                         data.totale_ospedalizzati.diff().iloc[-1], data.dimessi_guariti.diff().iloc[-1],
                                         data.tamponi.diff().iloc[-1], data.casi_testati.diff().iloc[-1],
                                         data.mortalita.diff().iloc[-1],
                                         data.intensivi.diff().iloc[-1], data.ricoverati.diff().iloc[-1],
                                         data.guariti.diff().iloc[-1]],
      'Variazione % rispetto a ieri': [data_pct.totale_casi.iloc[-1], data_pct.totale_positivi.iloc[-1],
                                       data_pct.nuovi_positivi.iloc[-1],
                                       data_pct.variazione_totale_positivi.iloc[-1], data_pct.deceduti.iloc[-1],
                                       data_pct.nuovi_decessi.iloc[-1], data_pct.terapia_intensiva.iloc[-1],
                                       data_pct.totale_ospedalizzati.iloc[-1], data_pct.dimessi_guariti.iloc[-1],
                                       data_pct.tamponi.iloc[-1], data_pct.casi_testati.iloc[-1],
                                       data_pct.mortalita.iloc[-1],
                                       data_pct.intensivi.iloc[-1], data_pct.ricoverati.iloc[-1],
                                       data_pct.guariti.iloc[-1]]
  }, index=['Totale casi', 'Attualmente positivi', 'Variazione totale casi', 'Variazione attualmente positivi',
            'Totale decessi',
            'Variazione decessi', 'Terapia intensiva', 'Ospedalizzati', 'Dimessi', 'Totale tamponi', 'Casi testati',
            'Mortalità', 'Critici', 'Ricoverati', 'Guariti'])

  pivot = pd.pivot_table(statistics, columns=['date'])
  pivot.sort_values(axis=1, by=['date'], ascending=False, inplace=True)
  pivot.columns = pivot.columns.strftime('%d/%m/%Y')

  return (recap, pivot)

def update_data():
    """ Augment dataset. """
    global data_pct, statistics, recap, pivot
    add_columns(data)
    data_pct = calc_percentages(data)
    statistics = calc_statistics(data)
    recap, pivot = calc_recap()

def base_seir_model(init_vals, params, t):
    """
    SEIR infection model.

    Params value for coronavirus (estimates):
      alpha = 0.189 # 1 / incubation_period  (1/5.3 days)
      beta = 1.2 # average contact rate of the population (gamma * R0)
      gamma = 0.0166 # 1 / latent_time (1/60 days)
      R0 = beta / gamma (2.6 - 4.34).

      initial values:
      S_0 = 1 - 222/60360000 # susceptibles
      E_0 = 1 / 60360000 # exposed
      I_0 = 200 # infected
      R_0 = 0 # recovered,
    """
    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (beta * S[-1] * I[-1]) * dt
        next_E = E[-1] + (beta * S[-1] * I[-1] - alpha * E[-1]) * dt
        next_I = I[-1] + (alpha * E[-1] - gamma * I[-1]) * dt
        next_R = R[-1] + (gamma * I[-1]) * dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    return np.stack([S, E, I, R]).T


def seir_model_with_soc_dist(init_vals, params, t):
    """ 
    SEIR infection model with social distancing.

    rho = social distancing factor.

    """

    S_0, E_0, I_0, R_0 = init_vals
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    alpha, beta, gamma, rho = params
    dt = t[1] - t[0]
    for _ in t[1:]:
        next_S = S[-1] - (rho * beta * S[-1] * I[-1]) * dt
        next_E = E[-1] + (rho * beta * S[-1] * I[-1] - alpha * E[-1]) * dt
        next_I = I[-1] + (alpha * E[-1] - gamma * I[-1]) * dt
        next_R = R[-1] + (gamma * I[-1]) * dt
        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    return np.stack([S, E, I, R]).T


def prepare_cases(cases, cutoff=25):
    """ clean cases per day for Rt estimation. """
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
                                 win_type='gaussian',
                                 min_periods=1,
                                 center=True).mean(std=2).round()

    idx_start = np.searchsorted(smoothed, cutoff)

    smoothed = smoothed.iloc[idx_start:]
    original = new_cases.loc[smoothed.index]

    return original, smoothed


def get_posteriors(sr, sigma=0.15):
    """ get posteriors for bayesian Rt estimation. """
    # (1) Calculate Lambda
    lambd = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))
    # (2) Calculate each day's likelihood
    likelihoods = pd.DataFrame(
            data=sps.poisson.pmf(sr[1:].values, lambd),
            index=r_t_range,
            columns=sr.index[1:])

    # (3) Create the Gaussian Matrix
    process_matrix = sps.norm(loc=r_t_range,
                              scale=sigma
                              ).pdf(r_t_range[:, None])

    # (3a) Normalize all rows to sum to 1
    process_matrix /= process_matrix.sum(axis=0)

    # (4) Calculate the initial prior
    # prior0 = sps.gamma(a=4).pdf(r_t_range)
    prior0 = np.ones_like(r_t_range) / len(r_t_range)
    prior0 /= prior0.sum()

    # Create a DataFrame that will hold our posteriors for each day
    # Insert our prior as the first posterior.
    posteriors = pd.DataFrame(
            index=r_t_range,
            columns=sr.index,
            data={sr.index[0]: prior0}
    )

    # We said we'd keep track of the sum of the log of the probability
    # of the data for maximum likelihood calculation.
    log_likelihood = 0.0

    # (5) Iteratively apply Bayes' rule
    for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):
        # (5a) Calculate the new prior
        current_prior = process_matrix @ posteriors[previous_day]

        # (5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
        numerator = likelihoods[current_day] * current_prior

        # (5c) Calcluate the denominator of Bayes' Rule P(k)
        denominator = np.sum(numerator)

        # Execute full Bayes' Rule
        posteriors[current_day] = numerator / denominator

        # Add to the running sum of log likelihoods
        log_likelihood += np.log(denominator)

    return posteriors, log_likelihood


def highest_density_interval(pmf, p=.9, debug=False):
    """ find highest density interval. """
    # If we pass a DataFrame, just call this recursively on the columns
    if isinstance(pmf, pd.DataFrame):
        return pd.DataFrame([highest_density_interval(pmf[col], p=p) for col in pmf],
                            index=pmf.columns)

    cumsum = np.cumsum(pmf.values)

    # N x N matrix of total probability mass for each low, high
    total_p = cumsum - cumsum[:, None]

    # Return all indices with total_p > p
    lows, highs = (total_p > p).nonzero()

    # Find the smallest range (highest density)
    best = (highs - lows).argmin()

    low = pmf.index[lows[best]]
    high = pmf.index[highs[best]]

    return pd.Series([low, high],
                     index=[f'Low_{p * 100:.0f}',
                            f'High_{p * 100:.0f}'])


def estimate_rt(df, sigma=0.15):
    """
    Bayesian estimation of Rt.
    df = data source
    sigma default = 0.15 (national estimate with best log likelihood)
  """
    _ , smoothed = prepare_cases(df.totale_casi)
    posteriors, _ = get_posteriors(smoothed, sigma=sigma)
    hdis = highest_density_interval(posteriors, p=.9)
    most_likely = posteriors.idxmax().rename('ML')
    result = pd.concat([most_likely, hdis], axis=1)

    return result


def calc_rt():
    global data

    _ , smoothed = prepare_cases(data.totale_casi)
    posteriors, _ = get_posteriors(smoothed)
    hdis = highest_density_interval(posteriors, p=.9)
    most_likely = posteriors.idxmax().rename('ML')
    result = pd.concat([most_likely, hdis], axis=1)

    print(result.tail())


@click.command()
@click.option('--region', '-r', help='Specify a region.')
@click.option('--rt', help='Estimate Rt.', is_flag=True)
def daily_stats(region=None, rt=False):
    """ 
    Daily stats for covid19 in Italy. 

    Available regions: Abruzzo, Basilicata, Calabria, Campania, Emilia-Romagna,
    'Friuli Venezia Giulia', Lazio, Liguria, Lombardia, Marche,
    Molise, 'P.A. Bolzano', 'P.A. Trento', Piemonte, Puglia,
    Sardegna, Sicilia, Toscana, Umbria, "Valle d'Aosta", Veneto.

    """

    if region:
        load_regional()
        set_region(region)
        update_data()
        print(f"Regione selezionata: {region}\n")

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
    print_last_day("Ingressi in intensiva: \t", 'ingressi_terapia_intensiva')
    print_last_day("Ospedalizzati: \t\t", 'totale_ospedalizzati')
    print_last_day("Dimessi: \t\t", 'dimessi_guariti')
    print_last_day("Totale tamponi: \t", 'tamponi')
    print_last_day("Tamponi per giorno: \t", 'tamponi_per_die')
    print_last_day("Totale testati: \t", 'casi_testati')
    print()

    print_as_pct("Morti: \t\t\t", 'mortalita')
    print_as_pct("Critici: \t\t", 'intensivi')
    print_as_pct("Ricoverati: \t\t", 'ricoverati')
    print_as_pct("Guariti: \t\t", 'guariti')
    print()

    if rt:
        calc_rt()

locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')
load()
update_data()
updated_at = data.date.iloc[-1].strftime('%d/%m/%Y')

if __name__ == "__main__":
    daily_stats()
# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
