import matplotlib.pyplot as plt
import matplotlib
from scipy.special import comb
import numpy as np

def triangular(periods):
    total = 0.0
    results = [total]
    for i in range(1, periods+1):
        total += 1/(comb(i+1, 2))
        results.append(total)
    normalizer = 21000000/max(results)
    results = [results[0]]+[i*normalizer for i in results[1:]]
    print(results[:5])
    return results

def _factorial(n):
    r = 1
    for i in range(1, n+1):
        r *= i
    return r

def factorial(periods):
    total = 0.0
    results = [total]
    for i in range(0, periods):
        total += 1/_factorial(i+1)
        results.append(total)
    normalizer = 21000000/max(results)
    results = [results[0]]+[i*normalizer for i in results[1:]]
    print(results[:5])
    return results

def power(base, periods):
    total = 0.0
    results = [total]
    for i in range(0, periods):
        total += 1/(base**i)
        results.append(total)
    normalizer = 21000000/max(results)
    results = [results[0]]+[i*normalizer for i in results[1:]]
    print(results[:5])
    return results

def square(power, periods):
    total = 0.0
    results = [total]
    for i in range(1, periods):
        total += 1/(i**power)
        results.append(total)
    normalizer = 21000000/max(results)
    results = [results[0]]+[i*normalizer for i in results[1:]]
    print(results[:5])
    return results

def satoshi(periods):
    f = 365*24*60/10
    total = 0.0
    results = [total]
    for i in range(periods):
        for j in range(4):
            total += f*50/(2**i)
            results.append(total)
    # results = [(i/21000000)*100 for i in results]
    results = [i/1000000 for i in results]
    print(results[:5])
    return results

def F(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return F(n-1)+F(n-2)

def AVAX_minting(periods, gov_switch):
    assert periods >= gov_switch
    minting_rate_function = np.linspace(1.02, 1.02, periods - gov_switch)
    print(minting_rate_function)
    results = triangular(periods)
    return results

def power_modified(periods):
    total = 0.0
    results = [total]
    first_phase = 4
    second_phase = 4
    third_phase = 22
    left_over = periods - (first_phase + second_phase + third_phase)
    # bases =         list(np.linspace(       2, 1.8, first_phase))
    # bases = bases + list(np.linspace(min(bases), 1.4, second_phase))
    # bases = bases + list(np.linspace(min(bases), 1.1, third_phase))
    # bases = bases + list(np.linspace(min(bases), 1.01, left_over))
    # bases = np.logspace(2, 1.1, first_phase+second_phase+third_phase)
    gamma = 1.15
    _lambda = 1.1
    bases = [gamma + (1/(1 + i**_lambda)) for i in range(0, periods)]
    # bases = bases + list(np.linspace(min(bases), 2, periods-30))
    bases = bases + [min(bases)]*(periods-30)
    print(bases)
    for i in range(0, periods):
        total += 1/(bases[i]**i)
        results.append(total)
    normalizer = 360000000/max(results)
    results = [i*normalizer/1000000 for i in results]
    # results = [i + 10 for i in results]
    # results = [(i/200000) for i in results]
    print("AVAX:", results[:50])
    return results

def power_modified_lower_bound(periods):
    total = 0.0
    results = [total]
    first_phase = 4
    second_phase = 4
    third_phase = 22
    left_over = periods - (first_phase + second_phase + third_phase)
    # bases =         list(np.linspace(       2, 1.8, first_phase))
    # bases = bases + list(np.linspace(min(bases), 1.4, second_phase))
    # bases = bases + list(np.linspace(min(bases), 1.1, third_phase))
    # bases = bases + list(np.linspace(min(bases), 1.01, left_over))
    # bases = np.logspace(2, 1.1, first_phase+second_phase+third_phase)
    gamma = 1.15
    _lambda = 1.1
    bases = [gamma + (1/(1 + i**_lambda)) for i in range(0, periods)]
    # bases = bases + list(np.linspace(min(bases), 2, periods-30))
    bases = bases + [min(bases)]*(periods-30)
    print(bases)
    for i in range(0, periods):
        total += 1/(bases[i]**i)
        results.append(total)
    normalizer = 360000000/max(results)
    results = [i*normalizer/1000000 for i in results]
    results = [i*0.5*0.9 for i in results]
    # results = [i + 10 for i in results]
    # results = [(i/200000) for i in results]
    print("AVAX:", results[:50])
    return results

def main():
    # font = {'family' : 'normal',
    #     'size'   : 20}

    # matplotlib.rc('font', **font)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    periods = 200
    gov_switch = 4
    # plt.plot(range(0,periods+1), triangular(periods), label="Triangular", color="blue")
    # plt.plot(range(0,periods+1), factorial(periods), label="Factorial", color="green")
    # plt.plot(range(0,periods+1), power(2, periods), label="Power 2 (2^i)", color="black",linestyle="--")
    # plt.plot(range(0,periods+1), power(1.2, periods), label="Power 1.1 (1.1^i)", color="black")

    # Plot AVAX full staking
    r = power_modified(periods)
    r = [((360 + i)/720) * 100 for i in r]
    plt.plot(range(0,periods+1), r, label="AVAX (100\% staked)", color="red", linestyle="-.")

    # Plot AVAX partial staking
    r = power_modified_lower_bound(periods)
    r = [((360 + i)/720) * 100 for i in r]
    plt.plot(range(0,periods+1), r, label="AVAX (50\% staked)", color="blue", linestyle="--")
    
    # plt.plot(range(0,periods), square(2, periods), label="Squares (i^2)", color="red")

    # Plot Bitcoin
    r = satoshi(int(periods/4))
    r = [i/(max(r)) * 100 for i in r]
    plt.plot(range(0, periods+1), r, label="BTC", color="orange", linestyle="-")
    
    # plt.plot(periods*[12.514285], color="gray", linestyle="--")
    # plt.plot(periods*[2*12.514285], color="gray", linestyle="--")
    # plt.plot(periods*[3*12.514285], color="gray", linestyle="--")
    # plt.plot(periods*[4*12.514285], color="gray", linestyle="--")
    # plt.plot(range(0, periods+1), AVAX_minting(periods, gov_switch), label="AVAX", color="blue", linestyle="--")

    plt.xlabel(r'Years Since Genesis', fontsize=32, labelpad=40)
    plt.ylabel(r'\% of Total Cap Reached', fontsize=32, labelpad=30)

    plt.tick_params(axis='both', 
        which='both', 
        # bottom='off', 
        top='off', 
        # labelbottom='off', 
        right='off', 
        # left='off', 
        # labelleft='off',
        labelsize=32
    )

    plt.legend(loc=4, prop={'size': 32})

    plt.xlim((0, 20))
    plt.ylim((-10, 110))
    plt.show()

if __name__ == "__main__":
    main()