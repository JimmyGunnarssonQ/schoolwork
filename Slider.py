import matplotlib.pyplot as plt 
from numpy import zeros, linspace
from matplotlib.widgets import Slider

beta = 45*1/100
alfa = 1/10*0.34
h = 1/10
def SIS(y,b):
    S,I = y
    N = S + I
    DSdt = -b*S*I/N + alfa*I
    DIdt = b*S*I/N - alfa*I
    return DSdt, DIdt
def Euler(ini,b):
    y = tuple(ini)
    K = 2
    Info = zeros((K,365*10))
    for k in range(365*10):
        for j in range(K):
            Info[j][k] = y[j]
        y = tuple(y[l] + h*SIS(y,b)[l] for l in range(len(y)))
    return Info[1]
Time = linspace(0,365,10*365)

y0 = 600000,3000
def rel(b):

    return [(600000+3000)*(1-alfa/b) for l in range(365*10)]

fig, ax = plt.subplots()
line, = plt.plot(Time, Euler(y0,beta), lw = 2, color = "maroon")
line2, = plt.plot(Time, rel(beta), "--", lw = 2, color = "black")
plt.grid()
plt.ylim([0,700000])
plt.xlabel("Time [days]")
plt.ylabel("People [count]")
plt.legend(["Infected", r"$N(1 - \frac{\beta}{\alpha})$"],title = "Information", bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.title("SIS model with variable " + r"$\beta$")

plt.subplots_adjust(left=0.25, bottom=0.25)
axSli = plt.axes([0.25, 0.1, 0.65, 0.1])
slid = Slider(ax = axSli, valmin = 0.06, valmax = 3, valinit = beta,label=r"$\beta$")
def update(v):
    line.set_ydata(Euler(y0, slid.val))
    line2.set_ydata(rel(slid.val))
    fig.canvas.draw_idle()
slid.on_changed(update)

plt.show()
