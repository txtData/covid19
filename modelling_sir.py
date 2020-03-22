import numpy as np
import matplotlib.pyplot as plt
#from scipy.integrate import odeint

# Total population, N.
N = 83000000
# Initial number of infected and recovered individuals, I0 and R0.
I0 = 22213 
R0 = 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta = 0.33
gamma = 1./12


# The SIR model differential equations.
def sir_deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def sir_non_deriv(days):
    infected = I0
    recovered = R0
    susceptible = S0
    s_s, i_s, r_s = [], [], []
    for i in range(0, days):
        susceptible_ = -beta * susceptible * infected / N
        infected_ = beta * susceptible * infected / N - gamma * infected
        recovered_ = gamma * infected
        susceptible = susceptible + susceptible_
        infected = infected + infected_
        recovered = recovered + recovered_
        s_s.append(susceptible)
        i_s.append(infected)
        r_s.append(recovered)
    return s_s, i_s, r_s

# non derivative version.
s, i, r = sir_non_deriv(160)

# A grid of time points (in days)
t = np.linspace(0, 159, 160)

# derivative version, integrate the SIR equations over the time grid, t.
#ret = odeint(sir_deriv, (S0, I0, R0), t, args=(N, beta, gamma))
#s, i, r = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd' ,axisbelow=True)
ax.plot(t, s, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, i, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, r, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set(yscale='log')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number')
ax.set_ylim(0,85000000)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()