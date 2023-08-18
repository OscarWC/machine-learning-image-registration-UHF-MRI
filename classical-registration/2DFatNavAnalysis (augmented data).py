import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image

differences = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
gtruths = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
regpar = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
differences1 = [] #differences for all datasets compiled together
for m in range(1,34):
    l = m - 1
    for i in range(1, 101):
        with open(f"2Dfatnav/train_{m}/00{i}_augments.txt") as f:
            lines = f.readlines()
            line1 = lines[0]
            r = float(line1.split("=")[1])

            line2 = lines[1]
            x = float(line2.split("=")[1])

            line3 = lines[2]
            y = float(line3.split("=")[1])
        with open(f"2Dfatnav/train_{m}/reg_00{i}.txt") as g:
            lines = g.readlines()
            line1 = lines[0]
            rr = float(line1.split("=")[1]) * (180/np.pi)

            line2 = lines[1]
            yr = float(line2.split("=")[1])

            line3 = lines[2]
            xr = float(line3.split("=")[1])


        #normalise each absolute difference to the ground truth parameter for that variable
        differences[l].append([np.abs((r - rr)/r), np.abs((x - xr)/x), np.abs((y - yr)/y)])
        #now getting the ground truth parameters out
        gtruths[l].append([r, x, y])
        #registration parameters
        regpar[l].append([rr, xr, yr])
        differences1.append([np.abs((r - rr)/r), np.abs((x - xr)/x), np.abs((y - yr)/y)])
#modified to calculate total stats rather than just per dataset
#separating the data out into lists for each difference in parameter - way to do this earlier on in the code?
n_map = ['rotation abs difference norm', 'x translation abs difference norm', 'y translation abs difference norm']
for n in range(3):
    data_xr = []
        #for i, difference in enumerate(differences[l]):
    for i, diff in enumerate(differences1):
        data_xr.append(diff[n])
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

        #text_file = open(f"2Dfatnav/analysis/statistics_{m}.txt", "a")
    text_file = open(f"2Dfatnav/analysis/statistics_total.txt", "a")

    text_file.write('\n')
    text_file.write(f"{n} Mean: {mean}\n")
    text_file.write(f"{n} Median : {median}\n")
    text_file.write(f"{n} Mode: {mode}\n")
    text_file.write(f"{n} SD: {stddev}\n")
    text_file.write(f"{n} Var: {variance}\n")

    #separating out the ground truth (gt) and registration parameters (rp). Plotting each variable for ground truth and registration values against index
    """o_map = ['rotation', 'x translation', 'y translation']
    m_map = ['rotation rp', 'x translation rp', 'y translation rp']
    for o in range(3):
        data_gt = []
        for i, gt in enumerate(gtruths[l]):
            data_gt.append(gt[o])
        index = np.arange(len(data_gt))

        data_rp = []
        for i, rp in enumerate(regpar[l]):
            data_rp.append(rp[o])
        index1 = np.arange(len(data_rp))

        o = o_map[o]
        # plot the data vs the index
        plt.scatter(data_gt, data_rp, label=f"{o}_{m}", color='red')
        # set the x and y axis labels
        plt.xlabel("Ground Truths", fontsize = 15)
        plt.ylabel("Registration Parameters", fontsize = 15)
        plt.xlim([-7, 7])
        plt.ylim([-7, 7])
        plt.legend(fontsize=15, loc='upper left')

        plt.plot([-7, 7], [-7, 7], linestyle='--', color='gray')

        plt.savefig(f'2Dfatnav/analysis/graph_{o}_{m}')
        plt.close()

    # form composite image to display all graphs in one
    images = [Image.open(f"2Dfatnav/analysis/graph_{o}_{m}.png") for o in o_map]

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

    new_image.save(f"2Dfatnav/analysis/graphs_{m}.png")"""