import numpy as np
import sir_modell as m
import datetime

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
