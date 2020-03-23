import load_covid_data as lcd
import helpers
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import sir_model as sir

# If true, new data is downloaded, if false the last downloaded data is used.
update_data = False 

predict_days = 230
truncate_infected = 2000

country = 'Germany'
population =  83200000
daily_increase = 0.33 # in not yet infected population
days_till_recovery = 12
critical_ratio = .05

icus = 28000
icu_availability_ratio = .20

def increase_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date += datetime.timedelta(days=1)
    return date.strftime('%Y-%m-%d')
   
def create_row(date, s, i, r):
    line =[
        date,
        "predicted",
        int(i+r),
        -1,
        int(s),
        int(i),
        int(r),
    ]
    return line


# load the data
if update_data:
    df = lcd.load_data_from_web()
    lcd.save_data(df)
df = lcd.load_data_from_file()
print('Last data for date:', df['date'].iloc[-1])


df = df[df['country'] == country]
df = df.loc[df.confirmed >= 100]
df = df.reset_index(drop=True)
df = df.drop(columns=['country', 'state', 'days_since_100'])

# Making sure columns confirm to SIR
df = df.rename(columns={'recovered': 'recovered_'})
df = df.assign(susceptible = population - df.confirmed)
df = df.assign(infected = df.confirmed - df.recovered_)
df = df.assign(recovered = df.recovered_)
df = df.drop(columns=['recovered_'])

date = df['date'].iloc[-1]
last_susceptible_count = df['susceptible'].iloc[-1]
last_infected_count =df['infected'].iloc[-1]
last_recovered_count = df['recovered'].iloc[-1]
s, i, r = sir.sir_non_deriv(predict_days, 
                  last_susceptible_count, 
                  last_infected_count, 
                  last_recovered_count,
                  daily_increase, 
                  1./days_till_recovery,
                  population)

for c in range(0,predict_days):
    date = increase_date(date)
    line = create_row(date, s[c], i[c], r[c])
    df.loc[len(df)] = line
    if i[c]<truncate_infected:
        break
    
df = df.assign(critical = df.infected * critical_ratio)
    
# set up plot    
palette = sns.hls_palette(1, l=.4, s=.8)
sns.set_palette(palette)
fig, ax = plt.subplots(figsize=(12, 8))    

# plot curves
#df['infected'].plot(label='infected', ls='-', lw=2.5)  
df['infected'].loc[df.type=='confirmed'].plot(label='cases confirmed', ls='-', lw=2.5)
df['infected'].loc[df.type=='predicted'].plot(label='cases predicted', ls='--', lw=2.5)
#df['recovered'].plot(label='recovered', ls='-', lw=2.5)

# plot ICUs
icus_available = icus * icu_availability_ratio * (1.0/critical_ratio)
print (icus_available)
icus_max = icus_available * 5
ax.axhline(icus_available, ls='-.', label='Available ICUs', lw=2.5)
ax.axhline(icus_max, ls=':', label='Available ICUs * 5', lw=2.5)

# configue axes
ax.set(yscale='log',
           title='Predicted active COVID-19 cases at a given time for Germany / intensive care unit (ICU) capacity',
           ylabel='Estimated cases (log scale)')
ax.set_ylim([100, 100000000])

interval = int(len(df)/10.0)

dates, ticks = helpers.create_dates(df['date'].iloc[0], interval, len(df))
ax.set_xticklabels(labels=dates)
ax.set_xticks(ticks=ticks)

ax.legend(loc='upper right', frameon=False)
sns.set()



  