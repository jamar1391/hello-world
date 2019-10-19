#! python3
"""
Zero-Based Execution -- helper script
"""

from matplotlib import pyplot as plt
import numpy as np
from itertools import combinations
import Fluor_script2 as fs


junctions = [0,
             10000,
             20000,
             30000,
             50000,
             80000,
             100000,
             110000,
             120000,
             150000,
             160000,
             180000,
             200000]

sections = []

for i in range(len(junctions) - 1):
    length = junctions[i + 1] - junctions[i]
    sections.append(length)


# Distance between junctions:
D1 = [0, 10000, 20000, 30000,
     50000, 80000, 100000, 110000,
     120000, 150000, 160000, 180000, 200000]

# Elevation at each junction:
y1 = [2000, 2000, 0, 0,
      500, 800, 1200, 1300,
      1350, 1800, 2000, 3250, 4000]

# Initial x-value at start:
x1 = [0]

# Derive x-values at junctions based on D and y:
for i in range(len(D1)-1):
    x_i = ((D1[i+1]-D1[i])**2 - (y1[i+1]-y1[i])**2)**(1/2) + x1[i]
    x1.append(x_i)

dx = 10  # size of sample along x-axis [ft]
n = (200000/dx)+1

# create n equally spaced partitions on x:
x = np.linspace(min(x1), max(x1), int(n))

# use more precise values to interpolate y and D at x:
y = np.interp(x,x1,y1)
D = np.interp(x,x1,D1)

locations = list(zip(x,y,D))  # y values are not unique but x and D are

########################################################################
# ZBE Stuff:
########################################################################

# These are all in psig--I learned how to use the Fathom software :)
# this is the list of maximum pressure in each pipe section
P_stat_max = [100, 908, 908, 879, 605, 389, 159, 87, 620, 340, 1030, 432]

# initialize dictionaries for different soil type characteristics:
slope = {'Silty Sand': 1,
         'Stable Rock': 10,
         'Medium Dense Sand': .66667,
         'Firm Clay': 1.3333} # max slope of soil type [v/h]

b_press = {'Silty Sand': 2000,
           'Stable Rock': 6000,
           'Medium Dense Sand': 2500,
           'Firm Clay': 1500} # b_press == max soil bearing pressure [psi]

cost_multiplier = {'Silty Sand': 1,
            'Stable Rock': 3,
            'Medium Dense Sand': 1,
            'Firm Clay': 1} # Excavation cost [$]

fnd_depth = {'Silty Sand': 4,
             'Stable Rock': 2,
             'Medium Dense Sand': 3,
             'Firm Clay': 3} # Foundation Depth [ft]

weight = {'Silty Sand': 99,
          'Stable Rock': 167,
          'Medium Dense Sand': 116,
          'Firm Clay': 106} # unit weight of soil [lb/ft3]

earth = []

# Assigns soil type to each discrete "chunk" along x, based on distance along pipeline:
for i in locations:
    if i[2] < 20001 or (120001 < i[2] < 150001):
        earth.append((i[2],'Silty Sand'))
    elif i[2] < 80001 or i[2] > 180001:
        earth.append((i[2],'Stable Rock'))
    elif i[2] < 120001:
        earth.append((i[2],'Medium Dense Sand'))
    else:
        earth.append((i[2],'Firm Clay'))

# initializes list of excavations based on starting location
exc = []

for i,j in enumerate(x[3000:-1020]): # for each starting location between 30000 and 189500:
    a = i + int(30000/dx)            # a = starting location index
    b = a + int(200/dx)              # b = ending location index (500 [ft] away)
    y0 = y[a]                        # the constant used as the base axis for integration
    A = 0                            # Accumulator for the area to be made flat
    B = 0                            # Accumulator for the area to be sloped based on soil type
    counter = 0
    if slope[earth[a][1]] == slope[earth[b][1]]: # if the slope stays the same, it's a 
        A = (y[b]-y[a])*200/2                    # simple triangle
        while y0 < y[b+counter]:
            B += (y[a+counter] - y0)*dx
            y0 += (slope[earth[a + counter][1]])*dx
            counter += 1
        exc.append(((A+B)*200,a)) # a 500x multiplier is applied to make the resulting flat area
                                  # 500'x500'
    else:
        for section in range(a,b):
            temp = ((1/2)*(y[section]+y[section+1])-y[a])*dx
            A += temp
        while y0 < y[a+counter]:
            B += (y[a+counter] - y0)*dx
            y0 += (slope[earth[a + counter][1]])*dx
            counter += 1
        exc.append(((A+B)*200,a))

x_locs      = []
exc_amounts = []

for i in exc:
    x_locs.append(i[1])
    exc_amounts.append(i[0])
	
plt.plot(fs.x_locs,fs.exc_amounts,color='r')
plt.plot(x_locs,exc_amounts,color='b')
plt.xlim([2500,16100])
plt.ylim([0,2000000])