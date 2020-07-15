import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 10000)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.plot(x, [2**(i+2) for i in x], label=r"2019", color="black", linestyle="-")
plt.plot(x, [2**(i+1) for i in x], label=r"2020", color="black", linestyle="--")
plt.plot(x, [2**(i) for i in x], label=r"2021", color="black", linestyle="-.")
plt.plot(x, [2**(i-1) for i in x], label=r"2022", color="black", linestyle=":")

plt.xlabel(r'Transactions / day', fontsize=32, labelpad=40)
plt.ylabel(r'\texttt{AVAX} / byte', fontsize=32, labelpad=30)
plt.ylim((0, 500))

plt.tick_params(axis='both', 
    which='both', 
    bottom='off', 
    top='off', 
    labelbottom='off', 
    right='off', 
    left='off', 
    labelleft='off')

plt.legend(loc=2, prop={'size': 32})
# plt.savefig('tex_demo')
plt.show()