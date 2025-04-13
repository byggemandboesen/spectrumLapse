import argparse

import matplotlib.pyplot as plt
import numpy as np


def main(args):
    data = np.load(args.i, allow_pickle=True)
    f, s, t = data["frequency"], data["observations"], data["timestamps"]

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(7,5), constrained_layout=True)
    ax.imshow(data["observations"], aspect="auto", extent=[f[0]/10**6, f[-1]/10**6, t.size, 0], cmap=args.cmap)

    # Configure timestamp axis
    n_time_labels = 7
    time_label_positions = np.round(np.linspace(0, t.size-1, n_time_labels, endpoint=True), 0).astype(int)
    time_labels = t[time_label_positions,0]
    ax.set_yticks(ticks=time_label_positions)
    ax.set_yticklabels(labels=time_labels, rotation=45)

    # Configure axis
    ax.set(xlabel="Frequency (MHz)", ylabel="Time (UTC)", title="Waterfall of observations")
    ax.minorticks_on()

    plt.savefig(args.o, dpi=200)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file", dest="i", default="out.npz", type=str)
    parser.add_argument("-o", help="Output file", dest="o", default="waterfall.png", type=str)
    parser.add_argument("-c", help="Waterfall colormap", dest="cmap", default="viridis", type=str)
    args = parser.parse_args()

    main(args)
