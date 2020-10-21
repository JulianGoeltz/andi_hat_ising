"""Make a cooling experiment."""
import logging
import numpy as np
import matplotlib.pyplot as plt
from bm_game import ising

logging.basicConfig(format='Cooling experiment -- %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# parameters
# expected critical temperature for w=1 is T_crit = 2.269
TEMP_HIGH = 6
TEMP_LOW = 0.01
STEPS = 40
BURN_IN = 10
MEASURE_UPDATES = 100
GRID_SIDE = 30


def main():
    """Run the cooling experiment and plot the result
    """

    # Initialize the experiment with a symmetric network
    bias_11 = 0
    weight_11 = 1
    weight = 4 * weight_11
    bias = 2 * bias_11 - 8 * weight_11
    temp_crit = weight_11 * 2 / np.log(1 + np.sqrt(2))
    logging.info("Initializing the network")
    network = ising.IsingModel(GRID_SIDE, bias=bias, conn_strength=weight)

    # loop and make the measurements
    temp_array = np.linspace(TEMP_HIGH, TEMP_LOW, STEPS)
    magn_arr = []
    for temp in temp_array:
        network.temp = temp
        logging.info(f"Running the temperature {temp}")

        # make the burn-in
        for _ in range(BURN_IN):
            network.update()

        # make updates and measure the magnetization
        magn = []
        for _ in range(MEASURE_UPDATES):
            network.update()
            magn.append(network.get_magnetization())
        magn_arr.append(magn)

    magn_arr = np.array(magn_arr)

    # plot the results
    logging.info("Plotting...")
    magn_mean = np.mean(magn_arr, axis=1)
    magn_std = np.std(magn_arr, axis=1)
    fig, axes = plt.subplots(1)
    axes.errorbar(temp_array, magn_mean, yerr=magn_std, color="tab:blue",
                linewidth=2)
    axes.vlines(temp_crit, -0.2, 1.2, colors="tab:orange", linewidth=2)
    axes.hlines(0.5, -0.2, TEMP_HIGH + 0.5, colors="black", linewidth=1,
                linestyle="--")
    axes.set_xlabel(r"Temperature $[1]$")
    axes.set_ylabel(r"Magnetization, normalized")
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.set_ylim([0.0, 1.1])
    axes.set_xlim([0.0, TEMP_HIGH + 0.3])
    axes.text(temp_crit + 0.2, 0.9, r"crit. temp., $T_{crit}$",
            horizontalalignment='left', color="tab:orange", fontweight="bold",
            fontsize=14)
    fig.savefig("magn_at_cooling.png")

    logging.info("Done")


if __name__ == '__main__':
    main()
