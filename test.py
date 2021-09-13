import matplotlib.pyplot as plt 
from numpy import zeros

iterations = int(input("Iterations count: "))
xtot = 365
h = xtot/iterations 
state1 = str(input("Do you wish to have default settings? ([Y]es/[N]o)"))
if state1 == "Y":
    beta = 45*1/100
    alfa = 1/10*0.34
    gamma = 1/10**4
    print("Spread rate: ", beta)
    print("Recovery of infected rate: ", alfa)
    print("Vaccination of susceptible rate: ", gamma)
if state1 == "N":
    beta = float(input("Spread rate: (relevant for 1 city model(s))"))
    alf = float(input("Recovery of infected rate:"))
    gam = float(input("Vaccination of susceptible rate (relevant for SIR):"))
CC = 1
print("The Euler steps have the size of:", h)
Time = list(i*h for i in range(0,iterations))
CityL = ["Ctesiphon", "Constantinople", "XD"]

def SIS(y):
    S,I = y
    N = S + I
    DSdt = -beta*S*I/N + alfa*I
    DIdt = beta*S*I/N - alfa*I
    return DSdt, DIdt

def Euler(ini,f):
    y = tuple(ini)
    K = len(f(y))
    Info = zeros((K,iterations))
    for k in range(iterations):
        for j in range(K*CC):
            Info[j][k] = y[j]
        y = tuple(y[l] + h*f(y)[l] for l in range(len(y)))
    return Info[1]

plt.figure(figsize=(8,8), dpi = 80)

plotconfig = str(input("Which simulation do you want? (SIS [SIS],SIR (Lecture Notes) [SIR], SIR [SIROG], SIR 2 cities [SIR2], SIR 2 cities (Lecture Notes) [SIRL2])"))
states = ["Susceptible", "Infected", "Recovered"]
colours = ["navy", "maroon", "limegreen", "b", "r", "g"]
print("Ok.")
if plotconfig == "SIS":
    CC = 1
    st = input("Default initial? [Y/N]")
    if st == "Y":
        ini = 600000,3000
    else:
        SU = int(input("Initial susceptible:"))
        IU = int(input("Initial infected:"))
        ini = SU, IU
    equ = input("[R]unge-[K]utta,[H]eun or [E]uler method?")
    if equ == "RK":
        A = RuKu(ini, SIS)
    if equ == "H":
        A = Heun(ini,SIS)
    if equ == "E":
        A = Euler(ini, SIS)
    if equ == "EE":
        A = Error(ini, SIS)
    if equ == "EE2":
        A = Error2(ini, SIS)
    for j in range(2):
        plt.plot(Time, A[j], color = colours[j], linewidth = 3, label = states[j])
    plt.title(plotconfig + " model")
    plt.plot([Time[0], Time[-1]], [(600000+3000)*(1 - alfa/beta), (600000+3000)*(1 - alfa/beta)], "--", color = "black", label = r"$N(1-\frac{\alpha}{\beta})$")
    if equ == "EE" or equ == "EE2":
        pass
    else:
        print("Ratio infected: ", float(A[1][-1]/(A[1][0] + A[0][0])))
        print("expected ratio: ", r"1 - \frac{\alpha}{\beta}")
    print("Done")
plt.legend(title = "Information", bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize='medium')
plt.grid()
plt.tight_layout()

plt.xlabel("Time [days]")
plt.ylabel("People [count]")
plt.show()