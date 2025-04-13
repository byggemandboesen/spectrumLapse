import argparse

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def animate(i, ax, line, f, s, t):
    line.set_data(f/10**6, s[i,:])
    ax.set(title=t[i,0])

    return line,

def main(args):
    data = np.load(args.i, allow_pickle=True)
    f, s, t = data["frequency"], data["observations"], data["timestamps"]

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(7,5), constrained_layout=True)
    line, = ax.plot([], [], color="b", lw=0.5)

    # Configure axis
    s_min, s_max = np.mean(np.min(s, axis=1)), np.max(s)
    s_range = np.abs(s_max-s_min)
    # ax.set(xlabel="Frequency (MHz)", ylabel="Amplitude (dB)", ylim=(s_min-0.1*s_range, s_max+0.1*s_range), xlim=(f[0]/10**6, f[-1]/10**6))
    ax.set(xlabel="Frequency (MHz)", ylabel="Amplitude (dB)", ylim=(s_min, s_max), xlim=(f[0]/10**6, f[-1]/10**6))

    ax.minorticks_on()
    ax.grid(alpha=0.5)

    anim = FuncAnimation(fig=fig, func=animate, frames=t.size, interval=10, blit=True, fargs=(ax, line, f, s, t))
    anim.save(args.o, dpi=200, writer=PillowWriter(fps=30))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file", dest="i", default="out.npz", type=str)
    parser.add_argument("-o", help="Output file", dest="o", default="timelapse.gif", type=str)
    args = parser.parse_args()

    main(args)
