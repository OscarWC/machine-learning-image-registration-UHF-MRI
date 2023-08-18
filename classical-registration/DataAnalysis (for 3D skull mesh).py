import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image

#number of images + 1
n = 101

#extracting data from folders. Key: nmi - n refers to the coordinate, m = r (rotation) or t (translation), i = nothing (ground truth) or r (registration parameters)
#loop over each file
differences = []
gtruths = []
regpar = []
for i in range(1, n):
    with open(f"folder2/00{i}_augments_reg.txt") as f:
        lines = f.readlines()
        line1 = lines[0]
        xr = float(line1.split("=")[1])

        line2 = lines[1]
        xt = float(line2.split("=")[1])

        line3 = lines[2]
        yr = float(line3.split("=")[1])

        line4 = lines[3]
        yt = float(line4.split("=")[1])

        line5 = lines[4]
        zr = float(line5.split("=")[1])

        line6 = lines[5]
        zt = float(line6.split("=")[1])
        #line7 is blank
        line8 = lines[7]
        xrr = float(line8.split("=")[1])

        line9 = lines[8]
        xtr = float(line9.split("=")[1])

        line10 = lines[9]
        yrr = float(line10.split("=")[1])

        line11 = lines[10]
        ytr = float(line11.split("=")[1])

        line12 = lines[11]
        zrr = float(line12.split("=")[1])

        line13 = lines[12]
        ztr = float(line13.split("=")[1])
    #normalise each absolute difference to the ground truth parameter for that variable
    differences.append([np.abs((xr - xrr)/xr), np.abs((xt - xtr)/xt), np.abs((yr - yrr)/yr), np.abs((yt -ytr)/yt), np.abs((zr - zrr)/zr), np.abs((zt - ztr)/zt)])
    #now getting the ground truth parameters out
    gtruths.append([xr, xt, yr, yt, zr, zt])
    #registration parameters
    regpar.append([xrr, xtr, yrr, ytr, zrr, ztr])

#using nested lists
#for i, difference in enumerate(differences):
    #print(f"differences {i}: {difference}")


#example for x rotation
#sum_xr = 0
#for difference in differences:
    #sum_xr += difference[0]
#print(f"Average difference in x rotation value between ground truth and registration is {sum_xr/n}")

#separating the data out into lists for each difference in parameter - way to do this earlier on in the code?
n_map = ['x rotation abs difference norm', 'x translation abs difference norm', 'y rotation abs difference norm', 'y translation abs difference norm', 'z rotation abs difference norm', 'z translation abs difference norm']
for n in range(6):
    data_xr = []
    for i, difference in enumerate(differences):
        data_xr.append(difference[n])
    #for labelling
    n = n_map[n]
    #analysis - rounding to 2 dp
    mean = np.mean(data_xr)
    mean = np.round(mean, 2)
    median = np.median(data_xr)
    median = np.round(median, 2)
    mode = stats.mode(data_xr)
    mode = mode.mode[0]
    mode = round(mode, 2)
    stddev = np.std(data_xr)
    stddev = np.round(stddev, 2)
    variance = np.var(data_xr)
    variance = np.round(variance, 2)

    text_file = open(f"analysis/statistics.txt", "a")

    text_file.write('\n')
    text_file.write(f"{n} Mean: {mean}\n")
    text_file.write(f"{n} Median : {median}\n")
    text_file.write(f"{n} Mode: {mode}\n")
    text_file.write(f"{n} SD: {stddev}\n")
    text_file.write(f"{n} Var: {variance}\n")

#separating out the ground truth (gt) and registration parameters (rp). Plotting each variable for ground truth and registration values against index
o_map = ['x rotation', 'x translation', 'y rotation', 'y translation', 'z rotation', 'z translation']
m_map = ['x rotation rp', 'x translation rp', 'y rotation rp', 'y translation rp', 'z rotation rp', 'z translation rp']
for o in range(6):
    data_gt = []
    for i, gt in enumerate(gtruths):
        data_gt.append(gt[o])
    index = np.arange(len(data_gt))

    data_rp = []
    for i, rp in enumerate(regpar):
        data_rp.append(rp[o])
    index1 = np.arange(len(data_rp))

    o = o_map[o]
    # plot the data vs the index
    plt.scatter(data_gt, data_rp, label=f"{o}", color='red')
    # set the x and y axis labels
    plt.xlabel("Ground Truths", fontsize = 15)
    plt.ylabel("Registration Parameters", fontsize = 15)

    plt.legend(fontsize=15, loc='upper left')

    plt.plot([-7, 7], [-7, 7], linestyle='--', color='gray')

    plt.savefig(f'analysis/graph_{o}')
    plt.close()

# form composite image to display all graphs in one
images = [Image.open(f"analysis/graph_{o}.png") for o in o_map]

widths, heights = zip(*(n.size for n in images))

total_width = max(widths) * 3
total_height = max(heights) * 2

new_image = Image.new('RGB', (total_width, total_height))

x_offset = 0
y_offset = 0
for i, image in enumerate(images):
    if i > 0 and i % 3 == 0:
        y_offset += max(heights)
        x_offset = 0
    new_image.paste(image, (x_offset, y_offset))
    x_offset += max(widths)

new_image.save("analysis/graphs.png")








    #plotting data - disabled this section for now
'''
    # fit data to a normal distribution
    mu, std = stats.norm.fit(data_xr)

    # generate evenly spaced numbers over the range of the data set
    x = np.linspace(min(data_xr), max(data_xr), 100)

    # calculate the PDF
    pdf = stats.norm.pdf(x, mu, std)

    plt.plot(x, pdf,)
    #plt.hist(data_xr, bins=50, density=True, alpha=0.5, label='Data histogram')
    plt.title(f"Probability Density Function for {n}")
    plt.xlabel(f"{n}")
    plt.ylabel("Probability")
    #plt.legend()
    #plt.show()
    plt.savefig(f'analysis/pdf_{n}')
    plt.close()

#form composite image to display all graphs in one
images = [Image.open(f"analysis/pdf_{n}.png") for n in n_map]

widths, heights = zip(*(n.size for n in images))

total_width = max(widths) * 3
total_height = max(heights) * 2

new_image = Image.new('RGB', (total_width, total_height))

x_offset = 0
y_offset = 0
for i, image in enumerate(images):
    if i > 0 and i % 3 == 0:
        y_offset += max(heights)
        x_offset = 0
    new_image.paste(image, (x_offset, y_offset))
    x_offset += max(widths)

new_image.save("analysis/pdfs.png")

'''


