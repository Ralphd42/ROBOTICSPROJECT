#Ralph Donato
#plotter 


import matplotlib.pyplot as plt
import numpy as np
import csv
# Data for plotting
#t = np.arange(0.0, 2.0, 0.01)
#s = 1 + np.sin(2 * np.pi * t)
with open('ThreeDPlotData') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    t=[]
    s=[]
    for row in csv_reader:
        t.append(float(row[3]))
        s.append(float(row[5]))
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='x', ylabel='Y',
       title='Range of motion')
    ax.grid()

    fig.savefig("THreeDPlotData.png")
    plt.show()