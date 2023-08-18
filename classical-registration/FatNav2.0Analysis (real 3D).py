import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image

numbers = [9, 10, 10, 4, 4, 4, 4, 4, 4, 10, 10, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 4, 4, 4, 6, 6, 6, 6]
xrs = []
xts = []
yrs = []
yts = []
zrs = []
zts = []
for m in range(1, 34):
    k = m - 1
    for i in range(1, numbers[k] + 1):
        with open(f"fatnavData/fn_{m}/reg_3D_00{i}.txt") as f:
            lines = f.readlines()
            #first line empty
            line1 = lines[1]
            xr = float(line1.split("=")[1])
            xrs.append(np.abs(xr))

            line2 = lines[2]
            xt = float(line2.split("=")[1])
            xts.append(np.abs(xt))

            line3 = lines[3]
            yr = float(line3.split("=")[1])
            yrs.append(np.abs(yr))

            line4 = lines[4]
            yt = float(line4.split("=")[1])
            yts.append(np.abs(yt))

            line5 = lines[5]
            zr = float(line5.split("=")[1])
            zrs.append(np.abs(zr))

            line6 = lines[6]
            zt = float(line6.split("=")[1])
            zts.append(np.abs(zt))

data_xr = [xrs, xts, yrs, yts, zrs, zts]
n_map = ['x rotation abs', 'x translation abs', 'y rotation abs', 'y translation abs', 'z rotation abs', 'z translation abs']
for n in range(0, 6):
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

    text_file = open(f"fatnavData/analysis/statistics.txt", "a")
    n = n_map[n]
    text_file.write('\n')
    text_file.write(f"{n} Mean: {mean}\n")
    text_file.write(f"{n} Median : {median}\n")
    text_file.write(f"{n} Mode: {mode}\n")
    text_file.write(f"{n} SD: {stddev}\n")
    text_file.write(f"{n} Var: {variance}\n")