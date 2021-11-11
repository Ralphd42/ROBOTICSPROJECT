#Ralph Donato
#Get max values from Inverse Kinematics file


import matplotlib.pyplot as plt
import numpy as np
import csv
 
maxX=0
maxY=0
maxZ=0

with open('invk.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    #t=[]
    #s=[]
    for row in csv_reader:
        x =float(row[0])
        y = float(row[1])
        z = float(row[2])
        if x >maxX:
            maxX=x
        if y>maxY:
            maxY=y
        if z>maxZ:
            maxZ= z

        
    print("x:{} y:{} z:{}".format(maxX,maxY,maxZ   ))
       