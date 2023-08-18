import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image

numbers = [9, 10, 10, 4, 4, 4, 4, 4, 4, 10, 10, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 4, 4, 4, 6, 6, 6, 6]
rs = []
xts = []
yts = []
for m in range(1, 34):
    k = m - 1
    for i in range(1, numbers[k] + 1):
        with open(f"fatnavData/fn_{m}/reg_00{i}.txt") as f:
            lines = f.readlines()
            line1 = lines[0]
            #get in degrees
            r = float(line1.split("=")[1]) * (180/np.pi)
            rs.append(np.abs(r))
            #parameters in registration parameters file are in Cartesian order so swapping round to my MRI orientation
            line2 = lines[1]
            yt = float(line2.split("=")[1])
            yts.append(np.abs(yt))

            line3 = lines[2]
            xt = float(line3.split("=")[1])
            xts.append(np.abs(xt))

data_xr = [rs, xts, yts]
n_map = ['rotation abs', 'x translation abs', 'y translation abs']
for n in range(0, 3):
    #for labelling
    #n = n_map[n]
    #analysis - rounding to 2 dp
    mean = np.mean(data_xr[n])
    mean = np.round(mean, 2)
    median = np.median(data_xr[n])
    median = np.round(median, 2)
    mode = stats.mode(data_xr[n])
    mode = mode.mode[0]
    mode = round(mode, 2)
    stddev = np.std(data_xr[n])
    stddev = np.round(stddev, 2)
    variance = np.var(data_xr[n])
    variance = np.round(variance, 2)

    text_file = open(f"fatnavData/analysis/statistics_2D.txt", "a")
    n = n_map[n]
    text_file.write('\n')
    text_file.write(f"{n} Mean: {mean}\n")
    text_file.write(f"{n} Median : {median}\n")
    text_file.write(f"{n} Mode: {mode}\n")
    text_file.write(f"{n} SD: {stddev}\n")
    text_file.write(f"{n} Var: {variance}\n")