import os, sys, time, argparse
sys.dont_write_bytecode = True

import numpy as np
import datetime

from src.soapy import SDR
import src.dsp as dsp

def main(args):
    # Initialize arrays
    observations = np.zeros((args.n, args.bins), dtype=np.float64)
    timestamps = np.zeros((args.n, 1), dtype="O")
    obs_sweeps = np.zeros((args.average, args.bins), dtype=np.float64)
    frequency = (args.fc+np.linspace(-args.sample_rate, args.sample_rate, args.bins)/2)*10**6

    sdr = SDR(driver=args.driver, freq=args.fc*10**6, sample_rate=args.sample_rate*10**6, bins=args.bins)
    for i in range(args.n):
        if args.release and i != 0:
            sdr = SDR(driver=args.driver, freq=args.fc*10**6, sample_rate=args.sample_rate*10**6, bins=args.bins)
        
        # Observe
        sdr.startStream()
        obs_time = datetime.datetime.now(tz=datetime.timezone.utc)
        timestamps[i,0] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%H:%M:%S")
        for j in range(args.average):
            obs_sweeps[j,:] = dsp.doFFT(bins=sdr.readFromStream(), n_bins=args.bins)
        observations[i,:] = np.mean(obs_sweeps, axis=0)
        sdr.stopStream()

        if args.release:
            del sdr
        
        # Wait until next observation
        next_obs = obs_time+datetime.timedelta(seconds=args.dt)
        sleep_time = (next_obs-datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds()
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
    
    np.savez(args.out, observations=observations, timestamps=timestamps, frequency=frequency)
    print("Finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Configure SDR
    parser.add_argument("-d", help="Soapy driver to use", dest="driver", required=True, type=str)
    parser.add_argument("-f", help="Center frequency of SDR (MHz)", dest="fc", default=1700, type=float)
    parser.add_argument("-s", help="Sample rate of SDR (MSPS)", dest="sample_rate", required=True, type=float)
    parser.add_argument("-r", help="Release SDR between observations", action="store_true", dest="release", default=False)

    # Sampling
    parser.add_argument("-b", help="Bins per sweep", dest="bins", default=16384, type=int)
    parser.add_argument("-a", help="Sweep averaging", dest="average", default=1, type=int)
    parser.add_argument("-n", help="Number of observations", dest="n", default=50, type=int)
    parser.add_argument("-t", help="Time between start of each observation (s)", dest="dt", default=10.0, type=float)

    # I/O
    parser.add_argument("-o", help="Name of output npz file", dest="out", default="out.npz", type=str)

    args = parser.parse_args()
    main(args)
