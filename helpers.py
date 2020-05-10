import numpy as np
import sir_model as m
import datetime

def print_growth_numbers(countries, df):
    df['newly_infected'] = df['confirmed'] - df['confirmed'].shift(1)
    print('\nGrowth of infections for different time periods:')
    print('Country         This Week     Last 3 days   Today         Last week')
    for i, country in enumerate(countries):
        df_country = df.loc[(df.country == country)]
        today = df_country.newly_infected.iloc[-1]
        yesterday = df_country.newly_infected.iloc[-2]
        minus3 = df_country.newly_infected.iloc[-4]
        minus7 = df_country .newly_infected.iloc[-8]
        minus14 = df_country.newly_infected.iloc[-15]
        
        inc_1day   = today / yesterday
        inc_3days  = today / minus3
        inc_weekly = today / minus7
        inc_week_before = minus7 / minus14
        
        inc_3days_per_day  = inc_3days**(1/3)
        inc_weekly_per_day = inc_weekly**(1/7)
        inc_wb_per_day = inc_week_before**(1/7)
        
        print(f'{country:15} {inc_weekly_per_day:.2f}          {inc_3days_per_day:.2f}          {inc_1day:.2f}          {inc_wb_per_day:.2f}')
        

def create_dates(start_date, step, length):
    date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    intervals = range(0,length,step)
    dates = []
    for i in intervals:
        if (length<250):
            dates.append(date.strftime('%b %d'))
        elif (length<500):
            dates.append(date.strftime('%b %d %Y'))
        else:
            dates.append(date.strftime('%b %Y'))
        date += datetime.timedelta(days=step)
    return dates, list(intervals)


def fit(target_series):
    best_loss = -1
    best_values = ()
    betas = np.linspace(0.380, 0.400, 101)
    for beta in betas:
        gammas = np.linspace(11, 12, 101)
        for gamma in gammas:
            gamma = 1./gamma
            _, i, _ = m.sir_non_deriv(160)
            loss = compute_quadratic_loss(target_series, i)
            if best_loss==-1 or loss<best_loss:
                best_loss = loss
                best_values = (beta, 1./gamma)
    # beta  = 0.3874, gamma = 1./11.64
    return best_values[0], best_values[1], best_loss


def compute_quadratic_loss(series1, series2):
    length = min(len(series1), len(series2))
    loss_sum = 0
    for i in range(length):
        loss = (series1[i]/1000-series2[i]/1000)**2
        loss_sum += loss
    loss_sum /= length
    return loss_sum
