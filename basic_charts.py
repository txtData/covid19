import load_covid_data as lcd
import helpers
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd


def case_plot():
    sns.set_palette(sns.hls_palette(len(countries)+1, l=.4, s=.8))
    fig, ax = plt.subplots(figsize=(12, 8))
    
    longest_line = 0
    for country in countries:
        df_country = df.loc[(df.country == country) & (df.confirmed >= 100)]
        df_country.reset_index()['confirmed'].plot(label=country, ls='-', lw=2.5)
        if df_country['deaths'].shape[0] > longest_line:
            longest_line = df_country['deaths'].shape[0]
    
    x = np.linspace(0, plt.xlim()[1] - 1)
    ax.plot(x, 100 * (1.33) ** x, ls='--', color='k', label='33% daily growth', lw=1.5)
    
    ax.set(yscale='log',
           title='Exponential growth of reported COVID-19 cases',
           xlabel='Days from first 100 confirmed cases',
           ylabel='Confirmed cases (log scale)')
    ax.set_xlim([0, longest_line])
    ax.set_ylim([100, 100000])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.legend(loc='lower right', frameon=False)
    sns.set()


def death_plot():
    sns.set_palette(sns.hls_palette(len(countries)+1, l=.4, s=.8))
    fig, ax = plt.subplots(figsize=(12, 8))
    
    longest_line = 0
    for country in countries:
        df_country = df.loc[(df.country == country) & (df.deaths >= 5)]
        df_country.reset_index()['deaths'].plot(label=country, ls='-', lw=2.5)
        if df_country['deaths'].shape[0] > longest_line:
            longest_line = df_country['deaths'].shape[0]
    
    x = np.linspace(0, plt.xlim()[1] - 1)
    ax.plot(x, 5 * (1.33) ** x, ls='--', color='k', label='33% daily growth', lw=1.5)
    
    ax.set(yscale='log',
           title='Total cumulative COVID-19 deaths by country',
           xlabel='Days from first 5 confirmed deaths',
           ylabel='Confirmed deaths (log scale)')
    ax.set_xlim([0, longest_line])
    ax.set_ylim([5, 10000])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.legend(loc='lower right', frameon=False)
    sns.set()
        
    
def critical_plot(df, p_crit=0.05):
    df = df.assign(critical_estimate=df.confirmed*p_crit)
    palette = sns.hls_palette(len(countries)+1, l=.4, s=.8)
    sns.set_palette(palette)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    df_pred = pd.DataFrame()
    for i, country in enumerate(countries):
        df_country = df.loc[(df.country == country)]
        df_country = df_country.tail(20)
        df_country.reset_index()['critical_estimate'].plot(label=country, color=palette[i], ls='-', lw=2.5)
        
        # compute estimates
        interval = 7
        last = df_country['critical_estimate'].iloc[-1]
        last2 = df_country['critical_estimate'].iloc[0-(1+interval)]   
        inc_weekly = last / last2
        inc_daily = inc_weekly**(1/interval)
        prediction = []
        index = []
        for j in range(0,20):
            prediction.append(last)
            last = last*inc_daily
            index.append(19+j)
        df_pred = pd.DataFrame(prediction, index=index, columns =['prediction']) 
        
        # plot estimates
        label = '_nolegend_'
        if i==len(countries)-1: 
            label = 'Prediction'
        df_pred['prediction'].plot(label=label, color=palette[i], ls=':', lw=2.5)
    
    # plot available ICUs
    for i, icus in enumerate(icus_per_country):
        label = '_nolegend_'
        if i==3: label = 'Available ICUs'
        ax.axhline(icus * icu_availability_ratio, color=palette[i], ls='-', label=label, lw=0.75)
    
    ax.set(yscale='log',
           title='Critical COVID-19 cases requiring intensive care units (ICUs) by country, estimated',
           ylabel='Estimated critical cases (log scale)')

    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlim([0, 0])
    
    dates, ticks = helpers.create_dates(df_country['date'].iloc[0], 2, 31)
    ax.set_xticklabels(labels=dates)
    ax.set_xticks(ticks=ticks)
    
    ax.legend(loc='lower right', frameon=False)
    sns.set()
 
    
if __name__ == '__main__':    
    countries = ['Italy', 'Germany', 'US (total)', 'United Kingdom (total)', 'Spain']
    icus_per_country = [7580, 28000, 115500, 4360]
    icu_availability_ratio = .20
 
    df = lcd.load_data_from_web()
    lcd.save_data(df)
    df = lcd.load_data_from_file()
    print('Last data for date:', df['date'].iloc[-1])

    df = df[df['country'].isin(countries)]
    df['country'].replace({'US (total)': 'US', 'United Kingdom (total)': 'UK'}, inplace=True)
    countries = ['Italy', 'Germany', 'US', 'UK'] # redefining countries, now that we changed the data frame
    
    case_plot()    
    death_plot()
    critical_plot(df)
    
