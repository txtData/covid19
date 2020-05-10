import load_covid_data as lcd
import helpers
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np


def cumulative_plot(df, to_plot='confirmed', title='', countries=['Germany'], frm=100):
    sns.set_palette(sns.hls_palette(len(countries)+1, l=.4, s=.8))
    fig, ax = plt.subplots(figsize=(12, 8))
    
    max_x = 0
    max_y = 0
    for country in countries:
        df_country = df.loc[(df.country == country) & (df[to_plot] >= frm)]
        df_country.reset_index()[to_plot].plot(label=country, ls='-', lw=2.5)
        if df_country['deaths'].shape[0] > max_x:
            max_x = df_country['deaths'].shape[0]
        if df_country[to_plot].max() > max_y:
            max_y = df_country[to_plot].max()
    
    x = np.linspace(0, plt.xlim()[1] - 1)
    ax.plot(x, frm * 1.33 ** x, ls='--', color='k', label='33% daily growth', lw=1.5)
    
    ax.set(yscale='log',
           title=title,
           xlabel='Days from first '+str(frm)+' confirmed cases',
           ylabel='Confirmed cases (log scale)')
    ax.set_xlim([0, max_x])
    ax.set_ylim([frm, max_y * 1.2])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.legend(loc='lower right', frameon=False)
    sns.set()
    plt.show()


def new_plot(df, to_plot='new_deaths', title='', countries=['Germany']):
    lcd.add_new_deaths(df)
    df['rolling'] = df[to_plot].rolling(10).mean()

    palette = sns.hls_palette(len(countries), l=.4, s=.8)
    sns.set_palette(palette)
    fig, ax = plt.subplots(figsize=(12, 8))

    max_x = 0
    max_y = 0
    for country in countries:
        df_country = df.loc[(df.country == country) & (df.date >= '2020-03-01')]
        df_country.reset_index()['rolling'].plot(label=country + ' (smoothed)', ls='-', lw=2.5)
        if df_country['deaths'].shape[0] > max_x:
            max_x = df_country['deaths'].shape[0]
        if df_country[to_plot].max() > max_y:
            max_y = df_country[to_plot].max()
    for country in countries:
        df_country = df.loc[(df.country == country) & (df.date >= '2020-03-01')]
        df_country.reset_index()[to_plot].plot(label=country, ls=':', lw=1.0)

    ax.set(title=title,
           xlabel='Time',
           ylabel='Confirmed new cases')
    ax.set_xlim([0, max_x])
    ax.set_ylim([0, max_y])
    dates, ticks = helpers.create_dates(df_country['date'].iloc[0], 5, len(df_country))
    ax.set_xticklabels(labels=dates)
    ax.set_xticks(ticks=ticks)
    ax.legend(loc='upper left', frameon=False)
    sns.set()
    plt.show()


if __name__ == '__main__':    
    df = lcd.load_data_from_web()
    lcd.save_data(df)
    df = lcd.load_data_from_file()
    print('Last data for date:', df['date'].iloc[-1])

    countries = ['Italy', 'Germany', 'US', 'United Kingdom']
    helpers.print_growth_numbers(countries, df)
    cumulative_plot(df, to_plot='confirmed', title='Cumulative reported COVID-19 cases', countries=countries, frm=100)
    cumulative_plot(df, to_plot='deaths', title='Cumulative reported COVID-19 deaths', countries=countries, frm=5)

    countries = ['Italy', 'Germany', 'United Kingdom']
    new_plot(df, to_plot='newly_infected', title='Daily new infections of COVID-19 cases', countries=countries)
    new_plot(df, to_plot='new_deaths', title='Daily COVID-19 deaths', countries=countries)

